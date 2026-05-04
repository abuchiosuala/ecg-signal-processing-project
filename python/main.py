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
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--windowSize", type=int, default=10)  # moving average
    parser.add_argument("--savWindowSize", type=int, default=11)  # savitzky-golay
    parser.add_argument("--quailityFactor", type=int, default=30)
    parser.add_argument("--notchFreq", type=int, default=60)
    parser.add_argument("--polyOrder", type=int, default=3)

    parser.add_argument("--no-gui",    action="store_true",
                        help="Print stats only, skip GUI")
    args = parser.parse_args()

    tData, sigData = loadData(args.filename, args.fs)

    # --- Add synthetic 60 Hz noise ---
    noise_30 = 0.1 * np.sin(2 * np.pi * 30 * tData)
    noise_60 = 0.1 * np.sin(2 * np.pi * 60 * tData)
    noise_drift = 0.5 * np.sin(2 * np.pi * 0.1 * tData)

    # random gaussian noise — what moving average handles
    noise_random = 0.3 * np.random.randn(len(tData))
    noisy_signal = sigData + noise_60

    # Filtering + peak detection

    # BUTTERWORTH FILTER
    s = butterFilter(sigData, args.fs, lowcut=args.lowcut,
                         highcut=args.highcut, order=args.order)
    # MOVING AVG FILTER
    test = movingAverageFilter(sigData, args.windowSize)

    # NOTCH FILTER
    notch = notchFilter(sigData, args.fs, args.quailityFactor, args.notchFreq)

    # SAVITZKYGOLAY FILTER
    sav = savitzkyGolayFilter(sigData, args.savWindowSize, args.polyOrder)

    peaks = peakDetection(test, args.threshold)

    bpm, hrv, maxBpm, minBpm = extractInfo(peaks, tData)

    # Save filtered signal
    np.savetxt('ecgFiltered.csv', np.column_stack((tData, s)), delimiter=',')

    if not args.no_gui:
        launch(tData, noisy_signal, fs=args.fs,
               init_lowcut=args.lowcut, init_highcut=args.highcut,
               init_order=args.order,   init_threshold=args.threshold)