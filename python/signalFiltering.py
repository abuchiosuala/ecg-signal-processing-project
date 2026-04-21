# This file is for filtering data and detection peaks from ECG scans. Can add more functions for other medical signals
from scipy.signal import sosfiltfilt, butter
import numpy as np

def butterFilter(array, frequency, lowcut=0.5, highcut=40, order=4):
    """
        Applies a Butterworth bandpass filter to the ECG signal to reduce noise.
        Filters between 0.5 and 40 Hz, removing baseline wander and high frequency interference.
        Args:
            array: The raw ECG signal data as a list or array.
        Returns:
            A NumPy array containing the filtered ECG signal.
        """

    if lowcut >= highcut:
        raise ValueError("lowcut must be less than highcut")
    if highcut >= frequency / 2:
        raise ValueError("highcut must be less than Nyquist frequency")
    sos = butter(order, [lowcut, highcut], 'bandpass', output='sos', fs=frequency)
    signalArray = np.array(array, dtype=float)
    filteredArray = sosfiltfilt(sos, signalArray)
    return filteredArray

def peakDetection(array, threshold):
    """
    Identifies local maxima in signal data(peaks). With this information we can
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