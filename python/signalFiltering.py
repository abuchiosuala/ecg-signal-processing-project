"""
This file is for filtering data and detection peaks from ECG scans. Can add more functions for other medical signals.
This file also contains different types on signal processing functions ranging from beginner-friendly understanding to deeper understanding.
"""
from scipy.signal import sosfiltfilt, butter, iirnotch, filtfilt
import numpy as np

def movingAverageFilter(array, window_size=10):
    """
      Smooths a signal by averaging neighboring samples inside a sliding window.
      Good for removing high-frequency noise quickly without scipy.
      Args:
          array      : The raw signal data as a list or NumPy array.
          windowSize : Number of samples to average together (default 10).
                       Larger window = smoother signal but more detail lost.
      Returns:
          A NumPy array of the smoothed signal, same length as input.
          The edges are handled with 'same' mode so the output length matches.
      """
    signalArray = np.array(array)
    kernel = np.ones(window_size) / window_size
    return np.convolve(signalArray, kernel, "same")

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
    return np.array(peaks, dtype=int)

def notchFilter(array, quailityFactor=30, fs=360, notchFreq=60):
    """
        Removes a specific frequency from the signal using a notch (band-stop) filter.
        Used to eliminate power line interference — 60 Hz in North America, 50 Hz in Europe.
        This is very common in real medical devices like ECG machines and EEG headsets.
        Args:
            array         : The raw signal data as a list or NumPy array.
            frequency     : Sampling frequency in Hz.
            notchFreq     : The frequency to remove in Hz (default 60 Hz).
            qualityFactor : Controls how narrow the notch is. Higher = narrower.
                            A value of 30 removes a thin band right around notchFreq (default 30).
        Returns:
            A NumPy array with the target frequency removed.
        """
    signalArray = np.array(array)
    b, a = iirnotch(notchFreq, quailityFactor, fs)
    filteredArray = filtfilt(b, a, signalArray)
    return filteredArray





