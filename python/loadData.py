# This file is for loading data and can be used to add other functions to load other types of data
import numpy as np

def loadData(filename, frequency):
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
            time = index/frequency # Convert sample index to time in seconds (fs = 360 Hz)
            timeD.append(time)
            signalD.append(signal)
        if len(timeD) == len(signalD):
            print("Data loaded.\n")
    return np.array(timeD), np.array(signalD)