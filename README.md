# ECG Signal Processing Project

## Overview

This project is a Python-based ECG (electrocardiogram) signal processing application that loads raw ECG data, applies multiple filtering techniques, detects heartbeats (R-peaks), and computes key heart metrics.

The system also includes an interactive GUI for visualizing signals and a frequency-domain analysis using FFT to better understand noise and filtering effects.

---

## Features

* 📂 **Data Loading**

  * Load ECG data from CSV files

* 🔧 **Signal Filtering**

  * Butterworth bandpass filter (0.5–40 Hz typical ECG range)
  * Notch filter (removes 50/60 Hz powerline noise)
  * Moving average filter
  * Savitzky-Golay filter

* ❤️ **Peak Detection & Analysis**

  * Detect R-peaks using local maxima
  * Compute:

    * Heart rate (BPM)
    * Heart rate variability (HRV)
    * Min/Max BPM

* 📊 **Interactive GUI**

  * Raw vs filtered signal visualization
  * Adjustable sliders for filter parameters
  * Region selection (zoom into signal segments)
  * Real-time stat updates

* 📈 **Frequency Analysis (FFT)**

  * Compare raw vs filtered frequency spectra
  * Visualize noise (e.g., 60 Hz interference)

* 🧪 **Unit Testing**

  * Tests for filtering, peak detection, data loading, and analysis

---

## Project Structure

```
python/
│
├── main.py               # Entry point
├── loadData.py           # CSV data loading
├── signalFiltering.py    # Filtering + peak detection
├── analysis.py           # BPM, HRV calculations
├── gui.py                # Visualization + interaction
├── test_functions.py     # Unit tests
└── ecgData/              # Sample ECG datasets
```

---

## How to Run

### Run the application

```
python3 main.py ecgData/101Ekg.csv
```

Optional arguments:

```
--fs 360
--lowcut 0.5
--highcut 40
--order 4
--threshold 0.5
--windowSize 10
--savWindowSize 11
--polyOrder 3
--qualityFactor 30
--notchFreq 60
```

---

### Run unit tests

```
python3 test_functions.py
```

---

## Example Workflow

1. Load ECG data
2. Apply filters (adjust sliders in GUI)
3. Detect peaks
4. View heart statistics
5. Use FFT to analyze frequency components

---

## Technologies Used

* Python
* NumPy
* SciPy
* Matplotlib

---

## Notes

* ECG signals are typically filtered between **0.5–40 Hz**
* Notch filtering removes **powerline interference (50/60 Hz)**
* FFT helps visualize frequency components and filtering effectiveness

---

## Author

Abuchi Osuala
