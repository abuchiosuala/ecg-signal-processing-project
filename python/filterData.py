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
            time = index/360.0
            timeD.append(time)
            signalD.append(signal)
        if len(timeD) == len(signalD):
            print("Data loaded.\n")
    return timeD, signalD

def butterFilter(array):
    sos = butter(4, [0.5, 40], 'bandpass', output='sos', fs=360)
    signalArray = np.array(array, dtype=float)
    filteredArray = sosfiltfilt(sos, signalArray)
    return filteredArray

def filterConvolve(signalArray, window=8):
    """
    Applies a moving average filter to the signal using convolution.
    Args:
        signalArray: List of signal amplitude values.
        window: Number of samples to average (default 8).
    Returns:
        Filtered signal as a numpy array.
    """
    windowSize = [1/window] * window
    signalArray = np.array(signalArray, dtype=float)
    filteredArray = np.convolve(signalArray, windowSize, 'same')
    return filteredArray

if __name__ == "__main__":
    # Argparse used to allow CLI arguments
    parser = argparse.ArgumentParser(description="Enter filename")
    parser.add_argument("filename", help="Path to ECG CSV file")
    args = parser.parse_args()
    tData, sigData = loadData(args.filename)
    # Filtering
    s = butterFilter(sigData)
    # s = filterConvolve(sigData)
    # Saving filtered data for peak detection
    np.savetxt('ecgFiltered.csv', np.column_stack((tData, s)), delimiter=',')
    # Convert list to numpy array for plotting
    tData = np.array(tData)
    sigData = np.array(sigData)
    sigData_centred = sigData - np.mean(sigData) 
    plt.figure(figsize=(12, 6))
    start, end = 0, 30
    plt.plot(tData, sigData_centred, label="Original", alpha=0.6)
    plt.xlim(start, end)
    plt.plot(tData, s, label="Filtered")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("ECG Signal: Original vs Filtered")
    plt.legend()
    plt.show()
