import numpy as np
import argparse
from loadData import loadData
from signalFiltering import butterFilter, peakDetection, movingAverageFilter, notchFilter, savitzkyGolayFilter
from analysis import extractInfo
from gui import launch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter filename")
    parser.add_argument("filename", help="Path to ECG CSV file")
    parser.add_argument("--fs",        type=float, default=360.0)
    parser.add_argument("--lowcut",    type=float, default=0.5)
    parser.add_argument("--highcut",   type=float, default=40.0)
    parser.add_argument("--order",     type=int,   default=4)
    parser.add_argument("--threshold", type=float, default=1.0)
    parser.add_argument("--windowSize", type=int, default=10)  # moving average
    parser.add_argument("--savWindowSize", type=int, default=11)  # savitzky-golay
    parser.add_argument("--quailityFactor", type=int, default=30)
    parser.add_argument("--notchFreq", type=int, default=60)
    parser.add_argument("--polyOrder", type=int, default=3)

    parser.add_argument("--no-gui",    action="store_true",
                        help="Print stats only, skip GUI")
    args = parser.parse_args()

    tData, sigData = loadData(args.filename, args.fs)

    # Filtering + peak detection

    # BUTTERWORTH FILTER
    s = butterFilter(sigData, args.fs, lowcut=args.lowcut,
                         highcut=args.highcut, order=args.order)
    # MOVING AVG FILTER
    test = movingAverageFilter(sigData, args.windowSize)

    # NOTCH FILTER
    notch = notchFilter(sigData, args.quailityFactor, args.fs, args.notchFreq)

    # SAVITZKYGOLAY FILTER
    sav = savitzkyGolayFilter(sigData, args.savWindowSize, args.polyOrder)

    peaks = peakDetection(sav, args.threshold)

    bpm, hrv, maxBpm, minBpm = extractInfo(peaks, tData)
    print(f"BPM:    {round(bpm, 2)}")
    print(f"HRV:    {round(hrv, 2)}")
    print(f"maxBpm: {round(maxBpm, 2)}")
    print(f"minBpm: {round(minBpm, 2)}")

    # Save filtered signal
    np.savetxt('ecgFiltered.csv', np.column_stack((tData, s)), delimiter=',')

    if not args.no_gui:
        launch(tData, sigData, fs=args.fs,
               init_lowcut=args.lowcut, init_highcut=args.highcut,
               init_order=args.order,   init_threshold=args.threshold)