# import numpy as np
# import argparse
# import matplotlib.pyplot as plt
#
# from loadData import loadData
# from signalFiltering import butterFilter, peakDetection
# from analysis import extractInfo
#
# if __name__ == "__main__":
#     # Argparse used to allow CLI arguments
#     parser = argparse.ArgumentParser(description="Enter filename")
#     parser.add_argument("filename", help="Path to ECG CSV file")
#     parser.add_argument("--fs", type=float, default=360.0)
#     args = parser.parse_args()
#     tData, sigData = loadData(args.filename, args.fs)
#
#     # Filtering
#     s = butterFilter(sigData, args.fs)
#
#     # Peak Detection
#     peaks = peakDetection(s, 1)
#
#     #Extrating info from peaks
#
#     bpm, hrv, maxBpm, minBpm = extractInfo(peaks, tData)
#     print(f"BPM: {round(bpm, 2)}")
#     print(f"HRV: {round(hrv, 2)}")
#     print(f"maxBpm: {round(maxBpm, 2)}")
#     print(f"minBpm: {round(minBpm, 2)}")
#
#     # Saving filtered data for peak detection
#     np.savetxt('ecgFiltered.csv', np.column_stack((tData, s)), delimiter=',')
#
#     # Subtract the mean to centre the signal around zero (removes DC offset/baseline shift)
#     sigDataCentred = sigData - np.mean(sigData)
#
#     # Stats figure
#     plt.figure(figsize=(6, 4))
#     ax = plt.gca()
#     ax.axis('off')
#     stats = [
#         ["Metric", "Value"],
#         ["Avg BPM", round(bpm, 2)],
#         ["HRV (ms)", round(hrv, 2)],
#         ["Max BPM", round(maxBpm, 2)],
#         ["Min BPM", round(minBpm, 2)],
#     ]
#     table = ax.table(cellText=stats, loc='center', cellLoc='center')
#     table.scale(1.5, 2)
#     ax.set_title("ECG Extracted Info")
#
#     # ECG figure
#     plt.figure(figsize=(12, 6))
#     start, end = 0, 30
#     plt.plot(tData, sigDataCentred, label="Original", alpha=0.6)
#     plt.xlim(start, end)
#     plt.plot(tData, s, label="Filtered")
#     plt.plot(tData[peaks], s[peaks], "x", color="red", markersize=10, label="Peaks")
#     plt.xlabel("Time (s)")
#     plt.ylabel("Amplitude")
#     plt.title("ECG Signal: Original vs Filtered")
#     plt.legend()
#     plt.show()  # Single call opens both figures

import numpy as np
import argparse
from loadData import loadData
from signalFiltering import butterFilter, peakDetection
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
    parser.add_argument("--no-gui",    action="store_true",
                        help="Print stats only, skip GUI")
    args = parser.parse_args()

    tData, sigData = loadData(args.filename, args.fs)

    # Filtering + peak detection (initial pass for CLI output)
    s = butterFilter(sigData, args.fs, lowcut=args.lowcut,
                         highcut=args.highcut, order=args.order)
    peaks = peakDetection(s, args.threshold)

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