# This file is for loading data and can be used to add other functions to load other types of data
import numpy as np
import csv

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
    with open(filename,  newline='') as csvfile:
        filereader = csv.reader(csvfile)
        next(filereader, None)  # skip header
        for line in filereader:
            if len(line) < 2:
                continue
            index = float(line[0])
            signal = float(line[1])
            time = index / frequency  # Convert sample index to time in seconds (fs = 360 Hz)
            timeD.append(time)
            signalD.append(signal)
        if len(timeD) == len(signalD):
            print("Data loaded.\n")
        return np.array(timeD), np.array(signalD)

