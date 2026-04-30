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
    rr_seconds = rr_seconds[(rr_seconds > 0.3) & (rr_seconds < 1.5)]
    bpm = np.mean(60/rr_seconds) # converting to BPM and taking avg
    HRV = np.std(rr_seconds) * 1000

    # Getting min and max heart beat
    all_bpms = 60 / rr_seconds
    mean_bpms = np.mean(all_bpms)
    data = []
    for x in all_bpms:
        if 1.5 * mean_bpms >= x >= mean_bpms / 2:
            data.append(x)
    maxBpm = np.max(data)
    minBpm = np.min(data)
    return bpm, HRV, maxBpm, minBpm
