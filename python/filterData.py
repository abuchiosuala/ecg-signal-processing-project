import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.signal import sosfiltfilt, butter

def loadData(filename):
    """
        Loads ECG data from a CSV file.
        Args:
            filename: Path to the CSV file containing ECG data.
        Returns:
            A tuple of two lists (timeData, signalData).
        """
    timeD = []
    signalD = []
    with open(filename, 'r') as f:
        print(next(f))  # discard first line
        for line in f:
            a, b, _, _ = line.split(',') # extra parameters are not needed
            index = float(a)
            signal = float(b)
            time = index/360.0 # Convert sample index to time in seconds (fs = 360 Hz)
            timeD.append(time)
            signalD.append(signal)
        if len(timeD) == len(signalD):
            print("Data loaded.\n")
    return timeD, signalD

def butterFilter(array):
    """
        Applies a Butterworth bandpass filter to the ECG signal to reduce noise.
        Filters between 0.5 and 40 Hz, removing baseline wander and high frequency interference.
        Args:
            array: The raw ECG signal data as a list or array.
        Returns:
            A NumPy array containing the filtered ECG signal.
        """
    sos = butter(4, [0.5, 40], 'bandpass', output='sos', fs=360)
    signalArray = np.array(array, dtype=float)
    filteredArray = sosfiltfilt(sos, signalArray)
    return filteredArray

def peakDetection(array, threshold):
    """
    Identifies local maximas in signal data(peaks). With this information we can
    extract information about the patient.
    Args:
            array: The list holding signal data.
            threshold: Determines what peaks to keep and what not.
    Returns: A list holding the peaks found in the data
    """
    peaks = []
    for index in range(1, len(array) - 1):
        if array[index] > array[index + 1] and array[index] > array[index -1] and array[index] > threshold:
            peaks.append(index)
    return peaks

def extractInfo(rPeaks):
    """
    Extracts meaningful health information from r-peak data.
    Computes average heart rate, heart rate variability (HRV), and the
    min/max instantaneous heart rate by analyzing the intervals between
    consecutive R-peaks.
    Args:
        rPeaks (array): 1D array of sample indices corresponding to detected R-peaks in the ECG signal.

    Returns:
        tuple:
            bpm: Average heart rate in beats per minute (BPM) computed as the mean of all BPMs.
            HRV: Heart rate variability in milliseconds (ms) computed as the standard deviation of rPeaks.
            maxBpm: Maximum heart rate in BPM.
            minBpm: Minimum heart rate in BPM.
    """
    rr_samples = np.diff(rPeaks) # Get RR(time interval between consecutive peaks)
    rr_seconds = rr_samples/360 # need to convert to seconds since my array are sample indices
    bpm = np.mean(60/rr_seconds) # converting to BPM and taking avg
    HRV = np.std(rr_samples) / 360 * 1000

    # Getting min and max heart beat
    rr_seconds = rr_samples / 360
    all_bpms = 60 / rr_seconds
    maxBpm = np.max(all_bpms)
    minBpm = np.min(all_bpms)
    return bpm, HRV, maxBpm, minBpm

if __name__ == "__main__":
    # Argparse used to allow CLI arguments
    parser = argparse.ArgumentParser(description="Enter filename")
    parser.add_argument("filename", help="Path to ECG CSV file")
    args = parser.parse_args()
    tData, sigData = loadData(args.filename)

    # Filtering
    s = butterFilter(sigData)

    # Peak Detection
    peaks = peakDetection(s, 1)

    #Extrating info from peaks
    bpm, hrv, maxBpm, minBpm = extractInfo(peaks)
    print(f"BPM: {round(bpm, 2)}")
    print(f"HRV: {round(hrv, 2)}")
    print(f"maxBpm: {round(maxBpm, 2)}")
    print(f"minBpm: {round(minBpm, 2)}")

    # Saving filtered data for peak detection
    np.savetxt('ecgFiltered.csv', np.column_stack((tData, s)), delimiter=',')

    # Convert list to numpy array for plotting
    tData = np.array(tData)
    sigData = np.array(sigData)

    # Subtract the mean to center the signal around zero (removes DC offset/baseline shift)
    sigDataCentred = sigData - np.mean(sigData)

    # Stats figure
    plt.figure(figsize=(6, 4))
    ax = plt.gca()
    ax.axis('off')
    stats = [
        ["Metric", "Value"],
        ["Avg BPM", round(bpm, 2)],
        ["HRV (ms)", round(hrv, 2)],
        ["Max BPM", round(maxBpm, 2)],
        ["Min BPM", round(minBpm, 2)],
    ]
    table = ax.table(cellText=stats, loc='center', cellLoc='center')
    table.scale(1.5, 2)
    ax.set_title("ECG Extracted Info")

    # ECG figure
    plt.figure(figsize=(12, 6))
    start, end = 0, 30
    plt.plot(tData, sigDataCentred, label="Original", alpha=0.6)
    plt.xlim(start, end)
    plt.plot(tData, s, label="Filtered")
    plt.plot(tData[peaks], s[peaks], "x", color="red", markersize=10, label="Peaks")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("ECG Signal: Original vs Filtered")
    plt.legend()
    plt.show()