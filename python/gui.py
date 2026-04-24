import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, SpanSelector

from signalFiltering import butterFilter, peakDetection
from analysis import extractInfo

## user drags on plot  →  on_select runs  →  zoom plot filled
## user moves slider   →  update runs     →  zoom plot re-synced with new filter

# function to run in main to display the gui
def launch(tData, sigData, fs=360.0, init_lowcut=0.5, init_highcut=40.0, init_order=4, init_threshold=1):

    # running the existing functions to get data about the signal filtering
    filtered = butterFilter(sigData, fs, lowcut=init_lowcut,
                               highcut=init_highcut, order=init_order)
    peaks = peakDetection(filtered, init_threshold)
    # This subtracts the average from the raw signal to remove the flat vertical shift
    raw_centred = sigData - np.mean(sigData)

    # ── figure + main axes ────────────────────────────────────────────────────
    # Here we begin to create the figure and axes of my plot
    # ax_ecg is the top plot and ax_zoom is the bottom plot
    fig, (ax_ecg, ax_zoom) = plt.subplots(2, 1, figsize=(12, 7), facecolor='lightskyblue')
    # making room for the sliders below and basically toggling margin and padding
    fig.subplots_adjust(left=0.1, right=0.75, bottom=0.35, hspace=0.5)

    # upper plot — full signal
    # Drawing the initial lines
    # First one is on the top plot

    # Unfiltered line
    line_raw,  = ax_ecg.plot(tData, raw_centred, color='tab:red',
                             alpha=0.4, lw=0.8, label='Raw')
    # Filtered line
    line_filt, = ax_ecg.plot(tData, filtered, color='tab:blue',
                             lw=1.2, label='Filtered')
    # Peaks
    scat_peaks = ax_ecg.scatter(tData[peaks], filtered[peaks],
                                marker='x', color='orange',
                                s=60, zorder=5, label='R-peaks')
    ax_ecg.set_xlim(tData[0], min(tData[-1], 30))
    ax_ecg.set_xlabel('Time (s)')
    ax_ecg.set_ylabel('Amplitude')
    ax_ecg.set_title('ECG — drag on this plot to select a region')
    ax_ecg.legend(fontsize=8)

    # lower plot — selected region

    # Currently empty until user selects spot on the top plot
    line_zfilt, = ax_zoom.plot([], [], color='tab:blue', lw=1.2)
    scat_zoom = ax_zoom.scatter([], [], marker='x', color='orange', s=60)
    ax_zoom.set_xlabel('Time (s)')
    ax_zoom.set_ylabel('Amplitude')
    ax_zoom.set_title('Selected region')

    # stats text (right of the plots)
    stats_ax = fig.add_axes([0.77, 0.35, 0.22, 0.55])
    stats_ax.axis('off')
    stats_text = stats_ax.text(0.05, 0.95, '', transform=stats_ax.transAxes,
                               va='top', fontsize=10, fontfamily='monospace')

    # function to display current stats whenever the data changes
    def show_stats(peaks, label='Full signal'):
        # Need 2 or more peaks to extract stats from
        if len(peaks) < 2:
            stats_text.set_text('Not enough peaks.')
            return
        # Get information given # of peaks
        bpm, hrv, hi, lo = extractInfo(peaks, tData)
        # Display the results
        stats_text.set_text(
            f'-- {label} --\n'
            f'Avg BPM : {bpm:.1f}\n'
            f'HRV     : {hrv:.1f} ms\n'
            f'Max BPM : {hi:.1f}\n'
            f'Min BPM : {lo:.1f}'
        )
    show_stats(peaks)

    # sliders
    ax_low = fig.add_axes([0.1,  0.24, 0.55, 0.03])
    ax_high = fig.add_axes([0.1,  0.19, 0.55, 0.03])
    ax_order = fig.add_axes([0.1,  0.14, 0.55, 0.03])
    ax_thr = fig.add_axes([0.1,  0.09, 0.55, 0.03])

    # Creating the actual slider and setting the appropriate vales
    sl_low = Slider(ax_low,   'Low-cut (Hz)',   0.1, 5.0,   valinit=init_lowcut)
    sl_high = Slider(ax_high,  'High-cut (Hz)',  5.0, 100.0, valinit=init_highcut)
    sl_order = Slider(ax_order, 'Filter order',   1,   8,     valinit=init_order, valfmt='%0.0f')
    sl_thr = Slider(ax_thr,   'Peak threshold', -2.0, 3.0,  valinit=init_threshold)

    # ── update — called whenever any slider moves ─────────────────────────────
    def update(val):
        # so given the value of the slider create a new filtered line
        new_filt  = butterFilter(sigData, fs,
                                 lowcut=sl_low.val,
                                 highcut=max(sl_high.val, sl_low.val + 0.5),
                                 order=max(1, int(round(sl_order.val))))
        # also recompute the peaks
        new_peaks = peakDetection(new_filt, sl_thr.val)

        # Updating the y-vales with the new line
        line_filt.set_ydata(new_filt)
        if len(new_peaks):
            # Set offsets lets me redraw my scatter plot without redrawing the whole plot
            scat_peaks.set_offsets(np.column_stack((tData[new_peaks], new_filt[new_peaks])))
        else:
            scat_peaks.set_offsets(np.empty((0, 2)))

        ax_ecg.relim()
        ax_ecg.autoscale_view()

        # keep zoom panel in sync if a region is selected
        # The span.extents are reading the yellow drag selection, so once they change this statement becomes Trie
        if span.extents[0] != span.extents[1]:
            # Getting the specific range the user chose
            t0, t1  = span.extents
            # Here we end up with every sample that falls within t0 and t1 because ths will return true for them
            # NumPy goes through every single element in tData and evaluates the condition, storing the result in a new array the exact same length:
            mask = (tData >= t0) & (tData <= t1)
            pk_mask = (tData[new_peaks] >= t0) & (tData[new_peaks] <= t1)
            # Setting filtered line with the new data for the zoom plot
            line_zfilt.set_data(tData[mask], new_filt[mask])

            if pk_mask.any():
                scat_zoom.set_offsets(np.column_stack((tData[new_peaks[pk_mask]], new_filt[new_peaks[pk_mask]])))
            else:
                scat_zoom.set_offsets(np.empty((0,2)))
            show_stats(new_peaks[pk_mask], label=f'{t0:.1f}s-{t1:.1f}s')
        else:
            show_stats(new_peaks)

        # store so on_select can read the latest filtered signal + peaks
        update.filtered = new_filt
        update.peaks = new_peaks
        fig.canvas.draw_idle()

    # seed before first slider move
    update.filtered = filtered
    update.peaks  = peaks

    # Whenever the slider moves run the update function
    sl_low.on_changed(update)
    sl_high.on_changed(update)
    sl_order.on_changed(update)
    sl_thr.on_changed(update)

    # reset button
    ax_reset  = fig.add_axes([0.77, 0.05, 0.1, 0.04])
    btn_reset = Button(ax_reset, 'Reset', hovercolor='0.975')

    def reset(event):
        sl_low.reset()
        sl_high.reset()
        sl_order.reset()
        sl_thr.reset()

        # clear the zoom plot
        line_zfilt.set_data([], [])
        scat_zoom.set_offsets(np.empty((0, 2)))
        ax_zoom.set_title('Selected region')
        fig.canvas.draw_idle()

        # Remove the zoom
        span.set_visible(False)
        span.extents = (0, 0)

        # Rest table data
        show_stats(update.peaks, label='Full signal')
        fig.canvas.draw_idle()


    btn_reset.on_clicked(reset)

    # ── SpanSelector — drag on upper plot to pick a region ────────────────────
    def on_select(t_min, t_max):
        # getting filtered data and peaks from the update function
        filt  = update.filtered
        peaks = update.peaks

        # Boolean to see if the values in the og data range fall between t-min and t-max
        # Here we end up with every sample that falls within t0 and t1 because ths will return true for them
        mask = (tData >= t_min) & (tData <= t_max)
        pk_sel = peaks[(tData[peaks] >= t_min) & (tData[peaks] <= t_max)]

        # using boolean indexing to only get the values that returned True
        line_zfilt.set_data(tData[mask], filt[mask])
        scat_zoom.set_offsets(
            np.column_stack((tData[pk_sel], filt[pk_sel]))
            if len(pk_sel) else np.empty((0, 2))
        )
        ax_zoom.set_xlim(t_min, t_max)
        ax_zoom.relim()
        ax_zoom.autoscale_view(scalex=False)
        ax_zoom.set_title(f'Selected: {t_min:.2f}s - {t_max:.2f}s')
        show_stats(pk_sel, label=f'{t_min:.1f}s-{t_max:.1f}s')
        fig.canvas.draw_idle()

    # keep span referenced — Python GC would destroy the widget otherwise
    span = SpanSelector(ax_ecg, on_select, direction='horizontal',
                        useblit=True, interactive=True,
                        props=dict(alpha=0.2, facecolor='gold'))
    plt.show()
    return span