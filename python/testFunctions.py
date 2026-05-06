import numpy as np
from signalFiltering import butterFilter, peakDetection, movingAverageFilter, notchFilter, savitzkyGolayFilter
from analysis import extractInfo
from loadData import loadData

# ----------------------------
# Invalid Input Tests
# ----------------------------
def testInvalidInputs():
    sig = np.random.randn(1000)
    # Butterworth invalid cutoffs
    butter_failed = False
    try:
        butterFilter(sig, frequency=100, lowcut=50, highcut=10)
    except ValueError:
        butter_failed = True
    assert butter_failed, "Butter filter should fail for invalid cutoffs"

    # Moving average invalid window
    movingAverageFailed = False
    try:
        movingAverageFilter(sig, window_size=0)
    except ValueError:
        movingAverageFailed = True
    assert movingAverageFailed, "Moving average should fail for invalid window size"

    # Notch invalid frequency
    notchFailed = False
    try:
        notchFilter(sig, fs=100, notchFreq=60)
    except ValueError:
        notchFailed = True
    assert notchFailed, "Notch filter should fail for invalid frequency"

    # Savitzky-Golay invalid window
    savitzkyFailed = False
    try:
        savitzkyGolayFilter(sig, windowSize=10, polyOrder=3)
    except ValueError:
        savitzkyFailed = True
    assert savitzkyFailed, "Savitzky-Golay should fail for even window size"

# ----------------------------
# butterFilter test
# ----------------------------
def testButterFilter():
    sig = np.sin(np.linspace(0, 10, 1000))
    filtered = butterFilter(sig, frequency=100)
    assert len(filtered) == len(sig), "Butter filter should not change signal length"

# ----------------------------
# peakDetection test
# ----------------------------
def testPeakDetection():
    # simple signal with obvious peaks
    sig = np.array([0, 1, 0, 2, 0, 1, 0])
    peaks = peakDetection(sig, threshold=0.5)
    assert np.array_equal(peaks, np.array([1, 3, 5])), "Peak detection failed on simple signal"

# ----------------------------
# extractInfo test
# ----------------------------
def testExtractInfo():
    # simulate peaks every 1 second → 60 BPM
    time = np.linspace(0, 10, 1000)
    sig = np.sin(2 * np.pi * 1 * time)
    peaks = peakDetection(sig, threshold=0.5)
    bpm, hrv, max_bpm, min_bpm = extractInfo(peaks, time)

    assert 50 < bpm < 70, "BPM should be around 60"
    assert hrv >= 0, "HRV should be non-negative"

# ----------------------------
# loadData test
# ----------------------------
def testLoadData():
    filename = "test_data.csv"

    with open(filename, "w") as f:
        f.write("index,signal\n")
        for i in range(100):
            f.write(f"{i},{np.sin(i)}\n")

    time, signal = loadData(filename, frequency=100)

    assert len(time) == len(signal), "Time and signal arrays should match"
    assert len(time) == 100, "Should load correct number of rows"

if __name__ == "__main__":
    testButterFilter()
    testPeakDetection()
    testExtractInfo()
    testLoadData()
    testInvalidInputs()
    print("All tests passed!")