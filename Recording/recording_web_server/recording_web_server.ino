#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <SPIFFS.h>
#include "driver/i2s.h"

// Wi-Fi and Web Server Configuration
const char *ssid = "Warning! MALWARE!"; // change according to requirements
const char *password = "Anu'shotspot";
const char *host = "esp32fs";
WebServer server(80);

// I2S pins
#define I2S_SCK 33 // Bit clock (BCLK)
#define I2S_SD 32 // Serial data (DOUT)
#define I2S_WS 15 // Word select (LRCL)

// Audio recording configuration
#define SAMPLE_RATE 16000 // 16kHz sample rate
#define CHUNK_DURATION 1 // 1 second duration
#define CHUNK_SIZE (SAMPLE_RATE * CHUNK_DURATION) // Number of samples for 1 second
#define TOTAL_DURATION 10 // seconds
#define RECORD_FILE "/recording.raw"

// Global variables
File recordFile;
int16_t audioBuffer[CHUNK_SIZE]; // Buffer to store audio
int seconds_passed = 0;
int total_bytes = 0;
bool isRecording = false;

// Format bytes for human-readable output
String formatBytes(size_t bytes) {
  if (bytes < 1024) {
    return String(bytes) + "B";
  } else if (bytes < (1024 * 1024)) {
    return String(bytes / 1024.0) + "KB";
  } else if (bytes < (1024 * 1024 * 1024)) {
    return String(bytes / 1024.0 / 1024.0) + "MB";
  } else {
    return String(bytes / 1024.0 / 1024.0 / 1024.0) + "GB";
  }
}

// Initialize I2S for audio recording
void initI2S() {
  // I2S configuration for INMP441
  i2s_config_t i2s_config = {
    .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_I2S),
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 1024,
    .use_apll = false
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
  i2s_set_clk(I2S_NUM_0, SAMPLE_RATE, I2S_BITS_PER_SAMPLE_16BIT, I2S_CHANNEL_MONO);
}

// Record audio for a specified duration
void recordAudio() {
  if (SPIFFS.exists(RECORD_FILE)) {
    SPIFFS.remove(RECORD_FILE);
  }

  recordFile = SPIFFS.open(RECORD_FILE, FILE_WRITE);
  if (!recordFile) {
    Serial.println("Failed to open file for recording!");
    return;
  }

  seconds_passed = 0;
  total_bytes = 0;
  isRecording = true;

  while (seconds_passed < TOTAL_DURATION) {
    size_t bytes_read;
    i2s_read(I2S_NUM_0, (void*)audioBuffer, sizeof(audioBuffer), &bytes_read, portMAX_DELAY);

    Serial.printf("Read %d bytes - %d seconds passed\n", bytes_read, seconds_passed);
    
    recordFile.write((uint8_t*)audioBuffer, bytes_read);
    total_bytes += bytes_read;

    seconds_passed++;
    delay(CHUNK_DURATION * 1000);
  }

  recordFile.close();
  isRecording = false;
  Serial.printf("Recording completed. Total bytes: %d\n", total_bytes);
}

// Web server handlers
void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 Audio Recorder</h1>";
  html += "<p>Current Recording Status: " + String(isRecording ? "Recording" : "Idle") + "</p>";
  html += "<p>Total Recorded Bytes: " + String(total_bytes) + "</p>";
  html += "<a href='/record'>Start Recording</a><br>";
  html += "<a href='/download'>Download Recording</a>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleRecord() {
  if (!isRecording) {
    server.send(200, "text/plain", "Starting recording...");
    recordAudio();
  } else {
    server.send(200, "text/plain", "Already recording");
  }
}

void handleDownload() {
  File file = SPIFFS.open(RECORD_FILE, "r");
  if (file) {
    server.sendHeader("Content-Type", "application/octet-stream");
    server.sendHeader("Content-Disposition", "attachment; filename=recording.raw");
    server.streamFile(file, "application/octet-stream");
    file.close();
  } else {
    server.send(404, "text/plain", "File not found");
  }
}

void setup() {
  Serial.begin(115200);

  // Initialize SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS initialization failed!");
    while (true);
  }

  // Initialize I2S
  initI2S();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  recordAudio();

  // Start mDNS
  if (MDNS.begin(host)) {
    Serial.println("MDNS responder started");
  }

  // Web server routes
  server.on("/", handleRoot);
  server.on("/record", handleRecord);
  server.on("/download", handleDownload);

  // Start server
  server.begin();
  Serial.println("HTTP server started");
  Serial.print("Open http://");
  Serial.print(host);
  Serial.println(".local in your browser");
}

void loop() {
  server.handleClient();
  delay(2);  // Allow CPU to switch to other tasks
}