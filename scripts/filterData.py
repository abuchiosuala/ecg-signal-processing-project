import numpy as np
import matplotlib.pyplot as plt

def loadData():
    # Open file and load data into lists
    # Break time and signal data into segments due to multiple recordings being concatenated in the CSV
    timeD = []
    signalD = []
    segmentsSeen = 0
    with open('ecgFiltered.csv', 'r') as f:
        prev_time = None
        for line in f:
            a, _, b = line.partition(',')
            a = float(a)
            b = float(b)

            if prev_time is not None and a < prev_time:
                segmentsSeen+=1
                if segmentsSeen == 100:
                    break

            timeD.append(a)
            signalD.append(b)
            prev_time = a
    return timeD, signalD

def filterConvolve(signalArray):
    # Convert list to numpy array
    signalArray = np.array(signalArray, dtype=float)
    # Use convolve (moving average filter) to remove unwanted noise
    filteredArray = np.convolve(signalArray, [0.2, 0.2, 0.2, 0.2, 0.2], 'same')
    return filteredArray

if __name__ == "__main__":
    tData, sigData = loadData()
    print(len(tData))
    print(len(sigData))

    s = filterConvolve(sigData)
    # Saving filtered data for peak detection
    np.savetxt('ecg_filtered.csv', np.column_stack((tData, s)), delimiter=',')
    # Convert list to numpy array for plotting
    tData = np.array(tData)
    sigData = np.array(sigData)
    plt.figure(figsize=(12, 6))
    plt.plot(tData, sigData, label="Original", alpha=0.6)
    plt.plot(tData, s, label="Filtered")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("ECG Signal: Original vs Filtered")
    plt.legend()
    plt.show()

