import librosa
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt


# Function to extract MFCC features from an audio file
def extract_features(audio_file, max_length):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=y))
    
    if mfccs.shape[1] < max_length:
        pad_width = max_length - mfccs.shape[1]
        mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mfccs = mfccs[:, :max_length]
        
    return np.concatenate((mfccs.flatten(), [spectral_centroid, spectral_bandwidth, zero_crossing_rate]))


# Corrected file paths
file_paths = [
'AudioFiles/DP75_N,N,P L U,73,F.wav',
'AudioFiles/BP61_COPD,E W,P R L ,53,M.wav',
'AudioFiles/EP15_Asthma,E W,P R U,49,F.wav',
'AudioFiles/BP32_N,N,A R L,30,M.wav',
'AudioFiles/DP14_Heart Failure,C,A R M,54,M.wav',
'AudioFiles/BP16_heart failure,C,P R U,56,M.wav',
'AudioFiles/BP111_COPD,E W,P R L ,51,M.wav',
'AudioFiles/BP103_N,N,P R U,81,F.wav',
'AudioFiles/EP80_asthma,E W,A L U,38,M.wav',
'AudioFiles/BP76_N,N,A L U,31,M.wav',
'AudioFiles/EP41_pneumonia,Crep,P R M,51,M.wav',
'AudioFiles/DP102_N,N,P L L,41,M.wav',
'AudioFiles/EP91_asthma,E W,P R U,43,F.wav',
'AudioFiles/BP108_COPD,E W,P R L ,63,M.wav',
'AudioFiles/BP53_asthma,E W,P R M,72,F.wav',
'AudioFiles/EP61_COPD,E W,P R L ,53,M.wav',
'AudioFiles/BP87_N,N,P R M,72,M.wav',
'AudioFiles/DP54_heart failure,Crep,P R L ,73,F.wav',
'AudioFiles/DP99_N,N,P R M,50,M.wav',
'AudioFiles/EP4_Heart Failure + Lung Fibrosis ,I C,P L R,72,F.wav',
'AudioFiles/EP13_Heart Failure,C,P L L,55,M.wav',
'AudioFiles/DP108_COPD,E W,P R L ,63,M.wav',
'AudioFiles/DP78_Asthma,E W,P R M,20,M.wav',
'AudioFiles/EP109_N,N,P L M,26,M.wav',
'AudioFiles/EP106_Asthma,E W,P L U,45,F.wav',
'AudioFiles/DP66_heart failure,Crep,P R L ,43,M.wav',
'AudioFiles/DP9_Asthma,E W,P R L ,59,M.wav',
'AudioFiles/EP87_N,N,P R M,72,M.wav',
'AudioFiles/DP67_heart failure,Crep,P R L ,24,F.wav',
'AudioFiles/EP97_Asthma,E W,P R U,24,M.wav',
'AudioFiles/EP56_asthma,E W,P R M,56,F.wav',
'AudioFiles/DP83_N,N,A R U,18,F.wav',
'AudioFiles/BP15_Asthma,E W,P R U,49,F.wav',
'AudioFiles/DP51_N,N,P L M,30,M.wav',
'AudioFiles/DP27_asthma,E W,P R M,53,F.wav',
'AudioFiles/DP21_BRON,Crep,P R L ,20,M.wav',
'AudioFiles/EP85_N,N,A R U,33,M.wav',
'AudioFiles/BP56_asthma,E W,P R M,56,F.wav',
'AudioFiles/EP100_N,N,P R M,70,F.wav',
'AudioFiles/DP16_heart failure,C,P R U,56,M.wav',
'AudioFiles/BP30_N,N,P R M,18,F.wav',
'AudioFiles/EP18_pneumonia,C,P R U,57,M.wav',
'AudioFiles/DP34_heart failure,Crep,P R M,78,F.wav',
'AudioFiles/DP7_Heart Failure + COPD,I C E W,P L R,65,M.wav',
'AudioFiles/EP26_Lung Fibrosis,Crep,P,90,F.wav',
'AudioFiles/DP97_Asthma,E W,P R U,24,M.wav',
'AudioFiles/BP45_heart failure,Crep,P R L ,30,M.wav',
'AudioFiles/DP74_N,N,P R M,74,M.wav',
'AudioFiles/DP17_COPD,E W,A R M,57,M.wav',
'AudioFiles/DP92_N,N,P L L ,43,M.wav',
'AudioFiles/EP83_N,N,A R U,18,F.wav',
'AudioFiles/EP38_Asthma,E W,P R M,38,M.wav',
'AudioFiles/EP110_COPD,E W,P L L,62,M.wav',
'AudioFiles/DP41_pneumonia,Crep,P R M,51,M.wav',
'AudioFiles/DP57_COPD,E W,P R L ,42,M.wav',
'AudioFiles/DP20_Asthma and lung fibrosis,C,A R M,90,M.wav',
'AudioFiles/EP12_Asthma,E W,P L L,50,F.wav',
'AudioFiles/EP42_heart failure,Crep,P L L,56,M.wav',
'AudioFiles/EP24_heart failure,Crep,P R L ,76,F.wav',
'AudioFiles/BP57_COPD,E W,P R L ,42,M.wav',
'AudioFiles/BP4_Heart Failure + Lung Fibrosis ,I C,P L R,72,F.wav',
'AudioFiles/DP90_heart failure,Crep,P L M,74,F.wav',
'AudioFiles/DP58_asthma,E W,P L M,40,M.wav',
'AudioFiles/BP77_Asthma,E W,A R L,40,M.wav',
'AudioFiles/BP96_N,N,P R L ,66,F.wav',
'AudioFiles/BP51_N,N,P L M,30,M.wav',
'AudioFiles/DP15_Asthma,E W,P R U,49,F.wav',
'AudioFiles/DP23_Lung Fibrosis,Crep,P R L ,50,M.wav',
'AudioFiles/EP27_asthma,E W,P R M,53,F.wav',
'AudioFiles/EP69_pneumonia,Bronchial,P R L ,64,M.wav',
'AudioFiles/DP24_heart failure,Crep,P R L ,76,F.wav',
'AudioFiles/BP75_N,N,P L U,73,F.wav',
'AudioFiles/EP44_asthma,E W,P R U,40,M.wav',
'AudioFiles/DP52_Lung Fibrosis,Crep,P L L,76,F.wav',
'AudioFiles/BP85_N,N,A R U,33,M.wav',
'AudioFiles/EP68_asthma,E W,P R L ,21,F.wav',
'AudioFiles/DP36_pneumonia,Crep,P R M,36,F.wav',
'AudioFiles/DP64_asthma,E W,P L U,60,M.wav',
'AudioFiles/BP25_copd,E W,P L L,76,M.wav',
'AudioFiles/BP13_Heart Failure,C,P L L,55,M.wav',
'AudioFiles/DP73_N,N,P L L,32,M.wav',
'AudioFiles/EP62_COPD,E W,P L M,53,M.wav',
'AudioFiles/BP101_Asthma,E W,P L M,12,F.wav',
'AudioFiles/BP17_COPD,E W,A R M,57,M.wav',
'AudioFiles/BP36_pneumonia,Crep,P R M,36,F.wav',
'AudioFiles/DP80_asthma,E W,A L U,38,M.wav',
'AudioFiles/EP57_COPD,E W,P R L ,42,M.wav',
'AudioFiles/EP14_Heart Failure,C,A R M,54,M.wav',
'AudioFiles/DP105_Lung Fibrosis,Crep,A U R,44,M.wav',
'AudioFiles/BP68_asthma,E W,P R L ,21,F.wav',
'AudioFiles/BP12_Asthma,E W,P L L,50,F.wav',
'AudioFiles/BP31_N,N,P L M,27,F.wav',
'AudioFiles/DP25_copd,E W,P L L,76,M.wav',
'AudioFiles/BP27_asthma,E W,P R M,53,F.wav',
'AudioFiles/DP26_Lung Fibrosis,Crep,P,90,F.wav',
'AudioFiles/EP31_N,N,P L M,27,F.wav',
'AudioFiles/EP9_Asthma,E W,P R L ,59,M.wav',
'AudioFiles/EP33_Asthma,E W,P R M,43,F.wav',
'AudioFiles/DP94_N,N,P L L,24,M.wav',
'AudioFiles/BP28_BRON,Crep,P L U,68,F.wav',
'AudioFiles/DP44_asthma,E W,P R U,40,M.wav',
'AudioFiles/DP61_COPD,E W,P R L ,53,M.wav',
'AudioFiles/BP44_asthma,E W,P R U,40,M.wav',
'AudioFiles/BP1_Asthma,I E W,P L L,70,M.wav',
'AudioFiles/EP45_heart failure,Crep,P R L ,30,M.wav',
'AudioFiles/DP42_heart failure,Crep,P L L,56,M.wav',
'AudioFiles/DP30_N,N,P R M,18,F.wav',
'AudioFiles/BP65_asthma,E W,P R L ,60,F.wav',
'AudioFiles/DP49_N,N,P R M,21,M.wav',
'AudioFiles/DP19_heart failure,C,P R U,70,F.wav',
'AudioFiles/EP92_N,N,P L L ,43,M.wav',
'AudioFiles/DP22_BRON,Crep,P R U,24,M.wav',
'AudioFiles/EP55_asthma,E W,P R U,72,F.wav',
'AudioFiles/DP28_BRON,Crep,P L U,68,F.wav',
'AudioFiles/DP37_pneumonia,Crep,A R L,70,F.wav',
'AudioFiles/BP55_asthma,E W,P R U,72,F.wav',
'AudioFiles/BP91_asthma,E W,P R U,43,F.wav',
'AudioFiles/BP42_heart failure,Crep,P L L,56,M.wav',
'AudioFiles/EP66_heart failure,Crep,P R L ,43,M.wav',
'AudioFiles/EP96_N,N,P R L ,66,F.wav',
'AudioFiles/DP69_pneumonia,Bronchial,P R L ,64,M.wav',
'AudioFiles/EP98_N,N,P L L,53,M.wav',
'AudioFiles/DP12_Asthma,E W,P L L,50,F.wav',
'AudioFiles/BP89_N,N,P L M,70,M.wav',
'AudioFiles/BP109_N,N,P L M,26,M.wav',
'AudioFiles/EP65_asthma,E W,P R L ,60,F.wav',
'AudioFiles/BP20_Asthma and lung fibrosis,C,A R M,90,M.wav',
'AudioFiles/BP110_COPD,E W,P L L,62,M.wav',
'AudioFiles/BP38_Asthma,E W,P R M,38,M.wav',
'AudioFiles/DP62_COPD,E W,P L M,53,M.wav',
'AudioFiles/DP13_Heart Failure,C,P L L,55,M.wav',
'AudioFiles/EP99_N,N,P R M,50,M.wav',
'AudioFiles/EP51_N,N,P L M,30,M.wav',
'AudioFiles/BP43_asthma,E W,P L M,15,M.wav',
'AudioFiles/EP28_BRON,Crep,P L U,68,F.wav',
'AudioFiles/EP21_BRON,Crep,P R L ,20,M.wav',
'AudioFiles/EP77_Asthma,E W,A R L,40,M.wav',
'AudioFiles/DP6_Plueral Effusion,I C B,P L R,81,M.wav',
'AudioFiles/DP48_N,N,P L U,31,M.wav',
'AudioFiles/BP59_heart failure,Crep,P R L ,83,F.wav',
'AudioFiles/DP59_heart failure,Crep,P R L ,83,F.wav',
'AudioFiles/DP32_N,N,A R L,30,M.wav',
'AudioFiles/BP74_N,N,P R M,74,M.wav',
'AudioFiles/BP49_N,N,P R M,21,M.wav',
'AudioFiles/BP7_Heart Failure + COPD,I C E W,P L R,65,M.wav',
'AudioFiles/BP22_BRON,Crep,P R U,24,M.wav',
'AudioFiles/DP79_asthma,E W,A R U,46,M.wav',
'AudioFiles/EP71_N,N,P R U,36,M.wav',
'AudioFiles/DP5_Heart Failure + COPD,I C E W,P L R ,71,M.wav',
'AudioFiles/DP31_N,N,P L M,27,F.wav',
'AudioFiles/BP81_N,N,P L U,33,M.wav',
'AudioFiles/BP24_heart failure,Crep,P R L ,76,F.wav',
'AudioFiles/BP106_Asthma,E W,P L U,45,F.wav',
'AudioFiles/EP81_N,N,P L U,33,M.wav',
'AudioFiles/EP111_COPD,E W,P R L ,51,M.wav',
'AudioFiles/DP47_asthma,E W,P L M,60,M.wav',
'AudioFiles/EP48_N,N,P L U,31,M.wav',
'AudioFiles/EP76_N,N,A L U,31,M.wav',
'AudioFiles/EP58_asthma,E W,P L M,40,M.wav',
'AudioFiles/DP72_N,N,P R U,24,F.wav',
'AudioFiles/BP46_asthma,E W,P L U,41,F.wav',
'AudioFiles/DP55_asthma,E W,P R U,72,F.wav',
'AudioFiles/EP2_Asthma,E W,P L L R,52,F.wav',
'AudioFiles/DP45_heart failure,Crep,P R L ,30,M.wav',
'AudioFiles/DP77_Asthma,E W,A R L,40,M.wav',
'AudioFiles/EP88_N,N,A R U,29,M.wav',
'AudioFiles/BP90_heart failure,Crep,P L M,74,F.wav',
'AudioFiles/BP102_N,N,P L L,41,M.wav',
'AudioFiles/BP82_N,N,P L U,38,M.wav',
'AudioFiles/BP10_Asthma,E W,P R U,59,M.wav',
'AudioFiles/DP100_N,N,P R M,70,F.wav',
'AudioFiles/BP94_N,N,P L L,24,M.wav',
'AudioFiles/EP8_Plueral Effusion,I C B,P L L,70,M.wav',
'AudioFiles/EP32_N,N,A R L,30,M.wav',
'AudioFiles/EP73_N,N,P L L,32,M.wav',
'AudioFiles/DP65_asthma,E W,P R L ,60,F.wav',
'AudioFiles/BP52_Lung Fibrosis,Crep,P L L,76,F.wav',
'AudioFiles/EP23_Lung Fibrosis,Crep,P R L ,50,M.wav',
'AudioFiles/BP35_Asthma,E W,A R L,38,M.wav',
'AudioFiles/DP81_N,N,P L U,33,M.wav',
'AudioFiles/EP89_N,N,P L M,70,M.wav',
'AudioFiles/DP3_Asthma,I E W,P L L R,50,F.wav',
'AudioFiles/DP68_asthma,E W,P R L ,21,F.wav',
'AudioFiles/DP29_heart failure,Crep,P L L,57,M.wav',
'AudioFiles/BP72_N,N,P R U,24,F.wav',
'AudioFiles/DP89_N,N,P L M,70,M.wav',
'AudioFiles/BP83_N,N,A R U,18,F.wav',
'AudioFiles/BP98_N,N,P L L,53,M.wav',
'AudioFiles/EP35_Asthma,E W,A R L,38,M.wav',
'AudioFiles/EP3_Asthma,I E W,P L L R,50,F.wav',
'AudioFiles/DP53_asthma,E W,P R M,72,F.wav',
'AudioFiles/EP84_N,N,A R U,65,F.wav',
'AudioFiles/DP2_Asthma,E W,P L L R,52,F.wav',
'AudioFiles/BP18_pneumonia,C,P R U,57,M.wav',
'AudioFiles/BP39_heart failure,Crep,P R L ,67,M.wav',
'AudioFiles/EP17_COPD,E W,A R M,57,M.wav',
'AudioFiles/DP10_Asthma,E W,P R U,59,M.wav',
'AudioFiles/DP63_COPD,E W,P R L ,58,F.wav',
'AudioFiles/DP40_heart failure,Crep,A R M,26,M.wav',
'AudioFiles/EP52_Lung Fibrosis,Crep,P L L,76,F.wav',
'AudioFiles/DP11_Heart Failure,C,P L L,53,M.wav',
'AudioFiles/DP106_Asthma,E W,P L U,45,F.wav',
'AudioFiles/DP71_N,N,P R U,36,M.wav',
'AudioFiles/DP98_N,N,P L L,53,M.wav',
'AudioFiles/EP5_Heart Failure + COPD,I C E W,P L R ,71,M.wav',
'AudioFiles/EP40_heart failure,Crep,A R M,26,M.wav',
'AudioFiles/BP66_heart failure,Crep,P R L ,43,M.wav',
'AudioFiles/DP85_N,N,A R U,33,M.wav',
'AudioFiles/BP29_heart failure,Crep,P L L,57,M.wav',
'AudioFiles/BP14_Heart Failure,C,A R M,54,M.wav',
'AudioFiles/DP1_Asthma,I E W,P L L,70,M.wav',
'AudioFiles/BP26_Lung Fibrosis,Crep,P,90,F.wav',
'AudioFiles/EP90_heart failure,Crep,P L M,74,F.wav',
'AudioFiles/DP104_Asthma,E W,P L U,45,F.wav',
'AudioFiles/BP62_COPD,E W,P L M,53,M.wav',
'AudioFiles/BP105_Lung Fibrosis,Crep,A U R,44,M.wav',
'AudioFiles/BP69_pneumonia,Bronchial,P R L ,64,M.wav',
'AudioFiles/DP56_asthma,E W,P R M,56,F.wav',
'AudioFiles/BP41_pneumonia,Crep,P R M,51,M.wav',
'AudioFiles/BP107_Asthma,E W,P L U,59,F.wav',
'AudioFiles/DP38_Asthma,E W,P R M,38,M.wav',
'AudioFiles/BP73_N,N,P L L,32,M.wav',
'AudioFiles/DP84_N,N,A R U,65,F.wav',
'AudioFiles/BP23_Lung Fibrosis,Crep,P R L ,50,M.wav',
'AudioFiles/EP63_COPD,E W,P R L ,58,F.wav',
'AudioFiles/BP48_N,N,P L U,31,M.wav',
'AudioFiles/BP58_asthma,E W,P L M,40,M.wav',
'AudioFiles/BP64_asthma,E W,P L U,60,M.wav',
'AudioFiles/DP18_pneumonia,C,P R U,57,M.wav',
'AudioFiles/EP47_asthma,E W,P L M,60,M.wav',
'AudioFiles/EP22_BRON,Crep,P R U,24,M.wav',
'AudioFiles/EP94_N,N,P L L,24,M.wav',
'AudioFiles/BP5_Heart Failure + COPD,I C E W,P L R ,71,M.wav',
'AudioFiles/DP50_N,N,P R L ,27,M.wav',
'AudioFiles/EP64_asthma,E W,P L U,60,M.wav',
'AudioFiles/EP16_heart failure,C,P R U,56,M.wav',
'AudioFiles/EP60_heart failure,Crep,P L L,83,F.wav',
'AudioFiles/BP97_Asthma,E W,P R U,24,M.wav',
'AudioFiles/BP95_N,N,P L M,18,M.wav',
'AudioFiles/DP88_N,N,A R U,29,M.wav',
'AudioFiles/EP46_asthma,E W,P L U,41,F.wav',
'AudioFiles/DP87_N,N,P R M,72,M.wav',
'AudioFiles/BP80_asthma,E W,A L U,38,M.wav',
'AudioFiles/EP112_N,N,P L M,30,M.wav',
'AudioFiles/DP93_N,N,P R M,75,M.wav',
'AudioFiles/EP50_N,N,P R L ,27,M.wav',
'AudioFiles/BP21_BRON,Crep,P R L ,20,M.wav',
'AudioFiles/BP19_heart failure,C,P R U,70,F.wav',
'AudioFiles/DP91_asthma,E W,P R U,43,F.wav',
'AudioFiles/DP46_asthma,E W,P L U,41,F.wav',
'AudioFiles/DP96_N,N,P R L ,66,F.wav',
'AudioFiles/BP70_N,N,P L U,52,F.wav',
'AudioFiles/DP8_Plueral Effusion,I C B,P L L,70,M.wav',
'AudioFiles/DP107_Asthma,E W,P L U,59,F.wav',
'AudioFiles/BP93_N,N,P R M,75,M.wav',
'AudioFiles/DP60_heart failure,Crep,P L L,83,F.wav',
'AudioFiles/BP33_Asthma,E W,P R M,43,F.wav',
'AudioFiles/EP37_pneumonia,Crep,A R L,70,F.wav',
'AudioFiles/BP6_Plueral Effusion,I C B,P L R,81,M.wav',
'AudioFiles/EP39_heart failure,Crep,P R L ,67,M.wav',
'AudioFiles/EP93_N,N,P R M,75,M.wav',
'AudioFiles/DP35_Asthma,E W,A R L,38,M.wav',
'AudioFiles/DP82_N,N,P L U,38,M.wav',
'AudioFiles/BP34_heart failure,Crep,P R M,78,F.wav',
'AudioFiles/BP86_N,N,P R U,68,F.wav',
'AudioFiles/BP40_heart failure,Crep,A R M,26,M.wav',
'AudioFiles/EP43_asthma,E W,P L M,15,M.wav',
'AudioFiles/EP78_Asthma,E W,P R M,20,M.wav',
'AudioFiles/BP60_heart failure,Crep,P L L,83,F.wav',
'AudioFiles/DP101_Asthma,E W,P L M,12,F.wav',
'AudioFiles/EP29_heart failure,Crep,P L L,57,M.wav',
'AudioFiles/EP53_asthma,E W,P R M,72,F.wav',
'AudioFiles/EP54_heart failure,Crep,P R L ,73,F.wav',
'AudioFiles/BP3_Asthma,I E W,P L L R,50,F.wav',
'AudioFiles/BP84_N,N,A R U,65,F.wav',
'AudioFiles/BP99_N,N,P R M,50,M.wav',
'AudioFiles/BP78_Asthma,E W,P R M,20,M.wav',
'AudioFiles/EP75_N,N,P L U,73,F.wav',
'AudioFiles/DP86_N,N,P R U,68,F.wav',
'AudioFiles/DP109_N,N,P L M,26,M.wav',
'AudioFiles/DP95_N,N,P L M,18,M.wav',
'AudioFiles/EP95_N,N,P L M,18,M.wav',
'AudioFiles/DP70_N,N,P L U,52,F.wav',
'AudioFiles/EP10_Asthma,E W,P R U,59,M.wav',
'AudioFiles/EP59_heart failure,Crep,P R L ,83,F.wav',
'AudioFiles/EP103_N,N,P R U,81,F.wav',
'AudioFiles/BP50_N,N,P R L ,27,M.wav',
'AudioFiles/EP79_asthma,E W,A R U,46,M.wav',
'AudioFiles/EP82_N,N,P L U,38,M.wav',
'AudioFiles/DP112_N,N,P L M,30,M.wav',
'AudioFiles/DP4_Heart Failure + Lung Fibrosis ,I C,P L R,72,F.wav',
'AudioFiles/EP105_Lung Fibrosis,Crep,A U R,44,M.wav',
'AudioFiles/BP54_heart failure,Crep,P R L ,73,F.wav',
'AudioFiles/BP92_N,N,P L L ,43,M.wav',
'AudioFiles/DP110_COPD,E W,P L L,62,M.wav',
'AudioFiles/EP101_Asthma,E W,P L M,12,F.wav',
'AudioFiles/EP19_heart failure,C,P R U,70,F.wav',
'AudioFiles/EP74_N,N,P R M,74,M.wav',
'AudioFiles/BP67_heart failure,Crep,P R L ,24,F.wav',
'AudioFiles/EP104_Asthma,E W,P L U,45,F.wav',
'AudioFiles/DP111_COPD,E W,P R L ,51,M.wav',
'AudioFiles/BP9_Asthma,E W,P R L ,59,M.wav',
'AudioFiles/BP11_Heart Failure,C,P L L,53,M.wav',
'AudioFiles/EP20_Asthma and lung fibrosis,C,A R M,90,M.wav',
'AudioFiles/DP33_Asthma,E W,P R M,43,F.wav',
'AudioFiles/EP1_Asthma,I E W,P L L,70,M.wav',
'AudioFiles/BP2_Asthma,E W,P L L R,52,F.wav',
'AudioFiles/BP104_Asthma,E W,P L U,45,F.wav',
'AudioFiles/BP112_N,N,P L M,30,M.wav',
'AudioFiles/BP8_Plueral Effusion,I C B,P L L,70,M.wav',
'AudioFiles/EP86_N,N,P R U,68,F.wav',
'AudioFiles/EP49_N,N,P R M,21,M.wav',
'AudioFiles/EP34_heart failure,Crep,P R M,78,F.wav',
'AudioFiles/BP100_N,N,P R M,70,F.wav',
'AudioFiles/BP71_N,N,P R U,36,M.wav',
'AudioFiles/BP37_pneumonia,Crep,A R L,70,F.wav',
'AudioFiles/BP88_N,N,A R U,29,M.wav',
'AudioFiles/DP103_N,N,P R U,81,F.wav',
'AudioFiles/EP25_copd,E W,P L L,76,M.wav',
'AudioFiles/BP79_asthma,E W,A R U,46,M.wav',
'AudioFiles/EP30_N,N,P R M,18,F.wav',
'AudioFiles/DP39_heart failure,Crep,P R L ,67,M.wav',
'AudioFiles/BP63_COPD,E W,P R L ,58,F.wav',
'AudioFiles/EP70_N,N,P L U,52,F.wav',
'AudioFiles/EP102_N,N,P L L,41,M.wav',
'AudioFiles/EP6_Plueral Effusion,I C B,P L R,81,M.wav',
'AudioFiles/EP72_N,N,P R U,24,F.wav',
'AudioFiles/EP11_Heart Failure,C,P L L,53,M.wav',
'AudioFiles/BP47_asthma,E W,P L M,60,M.wav',
'AudioFiles/DP76_N,N,A L U,31,M.wav',
'AudioFiles/EP7_Heart Failure + COPD,I C E W,P L R,65,M.wav',
'AudioFiles/DP43_asthma,E W,P L M,15,M.wav',
'AudioFiles/EP67_heart failure,Crep,P R L ,24,F.wav',
'AudioFiles/EP107_Asthma,E W,P L U,59,F.wav',
'AudioFiles/EP108_COPD,E W,P R L ,63,M.wav',
'AudioFiles/EP36_pneumonia,Crep,P R M,36,F.wav'
]

labels = [0, 1, 1, 0, 2, 2, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 2, 2, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 2, 0, 2, 0, 3, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 2, 1, 0, 0, 1, 2, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 2, 0, 1, 1, 1, 0, 1, 1, 2, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 1, 1, 1, 2, 0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 3, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 2, 0, 1, 1, 1, 0, 0, 2, 1, 0, 0, 3, 0, 0, 0, 0, 2, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 3, 0, 1, 2, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 2, 1, 1, 0, 0, 2, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 2, 0, 2, 1, 0, 3, 1, 0, 1, 1, 0]
features = []
for file in file_paths:
    mfcc_features = extract_features(file, 7500)
    features.append(mfcc_features)

# Convert to numpy array for sklearn
X = np.array(features)
y = np.array(labels)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the SVC model
model = SVC(kernel='linear', probability=True)

# Train the model
model.fit(X_train, y_train)

import pickle

with open('svm_model.pkl', 'wb') as f:
    pickle.dump(model, f)

if __name__ == "__main__":

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    print(classification_report(y_test, y_pred))


