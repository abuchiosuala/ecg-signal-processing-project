import numpy as np

def extractInfo(rPeaks, timeArray):
    """
    Extracts meaningful health information from r-peak data.
    Computes average heart rate, heart rate variability (HRV), and the
    min/max instantaneous heart rate by analyzing the intervals between
    consecutive R-peaks.
    Args:
            rPeaks (array): 1D array of sample indices corresponding to
                             detected R-peaks in the ECG signal.
            timeArray: array holding the time values for the ECG signal

    Returns:
        tuple:
            bpm: Average heart rate in beats per minute (BPM) computed as the mean of all BPMs.
            HRV: Heart rate variability in milliseconds (ms) computed as the standard deviation of RR intervals.
            maxBpm: Maximum heart rate in BPM.
            minBpm: Minimum heart rate in BPM.
    """
    peak_times = timeArray[rPeaks] # Get specific time at each peak using my time array
    rr_seconds = np.diff(peak_times) # Get RR(time interval between consecutive peaks)
    rr_seconds = rr_seconds[(rr_seconds > 0.3) & (rr_seconds < 1.5)] # this is to remove outliers this is a boolean mask returns TRUE for each one
    bpm = np.mean(60/rr_seconds) # converting to BPM and taking avg
    HRV = np.std(rr_seconds) * 1000

    # Getting min and max heart beat
    all_bpms = 60 / rr_seconds
    mean_bpms = np.mean(all_bpms)
    data = []
    for x in all_bpms: # this is to remove outliers due to skewed data
        if 1.5 * mean_bpms >= x >= mean_bpms / 2:
            data.append(x)
    maxBpm = np.max(data)
    minBpm = np.min(data)
    return bpm, HRV, maxBpm, minBpm

def extractFrequency(sigData, fs):
    """
    Computes the frequency spectrum of a signal using the Fast Fourier Transform (FFT).
    Converts the signal from the time domain into the frequency domain, allowing
    you to see which frequencies are present and how strong they are.
    Args:
        sigData : The signal data as a list or NumPy array.
        fs      : Sampling frequency in Hz.
    Returns:
        freqs     : NumPy array of frequency values in Hz (x axis).
        magnitude : NumPy array of magnitude values showing the strength
                    of each frequency (y axis).
    """
    freqs = np.fft.rfftfreq(len(sigData), 1/fs)
    magnitude = np.abs(np.fft.rfft(sigData))
    return freqs, magnitude