// script.js
document.addEventListener('DOMContentLoaded', function() {
    const audioUpload = document.getElementById('audio-upload');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');
    const toggleAnalysis = document.getElementById('toggle-analysis'); // Toggle button
    const circleDisabled = document.getElementById('circle-disabled');
    const circleEnabled = document.getElementById('circle-enabled');

    // Event listener for the toggle
    toggleAnalysis.addEventListener('change', () => {
        if (toggleAnalysis.checked) {
            // Show enabled circle, hide disabled circle
            circleDisabled.classList.add('hidden');
            circleEnabled.classList.remove('hidden');
            console.log('CNN model enabled');
        } else {
            // Show disabled circle, hide enabled circle
            circleDisabled.classList.remove('hidden');
            circleEnabled.classList.add('hidden');
            console.log('CNN model disabled');
        }
    });
    
    async function handleFileUpload(file) {
        if (!file) return;

        try {
            // Show loading state
            loadingElement.classList.remove('hidden');
            resultsElement.classList.add('hidden');

            // Prepare form data
            const formData = new FormData();
            formData.append('audio', file);
            formData.append('use_cnn', toggleAnalysis.checked);

            // Send request to server
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }

            displayResults(data);
        } catch (error) {
            console.error('Upload error:', error);
            showError(error.message || 'An error occurred during upload');
        } finally {
            loadingElement.classList.add('hidden');
        }
    }

    function displayResults(data) {
        // Update primary condition
        document.getElementById('primary-condition').textContent = data.primary_condition;
        
        // Update confidence score
        document.getElementById('confidence-value').textContent = `${data.confidence}% confidence`;
        document.getElementById('confidence-bar').style.width = `${data.confidence}%`;

        // Show results section
        resultsElement.classList.remove('hidden');
    }

    function showError(message) {
        alert(message);
    }

    // Event Listeners
    audioUpload.addEventListener('change', (e) => {
        handleFileUpload(e.target.files[0]);
    });

    // Drag and drop functionality
    const dropZone = document.querySelector('.upload-button');
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('bg-blue-100');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-blue-100');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-blue-100');
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });
});