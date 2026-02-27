import numpy as np
import matplotlib.pyplot as plt

def loadData():
    # Open file and load data into lists
    # Breaking (time and signal) data into segments due to multiple recordings being concatenated in the CSV
    timeD = []
    signalD = []
    with open('101_ekg.csv', 'r') as f:
        print(next(f))  # discard first line
        for line in f:
            a, b, c, _ = line.split(',')
            a = float(a)
            b = float(b)
            time = a/360.0
            timeD.append(time)
            signalD.append(b)
        if len(timeD) == len(signalD):
            print("Data loaded.\n")
    return timeD, signalD

def filterConvolve(signalArray):
    windowSize = [1/8] * 8
    # Convert list to numpy array in order to use convolve method
    signalArray = np.array(signalArray, dtype=float)
    # Use convolve (moving average filter) to remove unwanted noise and using same to return the same amount of lines
    filteredArray = np.convolve(signalArray, windowSize, 'same')
    return filteredArray

if __name__ == "__main__":
    tData, sigData = loadData()
    # Filtering
    s = filterConvolve(sigData)
    # Saving filtered data for peak detection
    np.savetxt('ecg_filtered.csv', np.column_stack((tData, s)), delimiter=',')
    # Convert list to numpy array for plotting
    tData = np.array(tData)
    sigData = np.array(sigData)
    plt.figure(figsize=(12, 6))
    start, end = 0, 30
    plt.plot(tData, sigData, label="Original", alpha=0.6)
    plt.xlim(start, end)

    plt.plot(tData, s, label="Filtered")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("ECG Signal: Original vs Filtered")
    plt.legend()
    plt.show()

