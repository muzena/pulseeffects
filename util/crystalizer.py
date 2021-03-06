#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavefile

rate, wave = wavefile.read('test.wav')

wave_y = wave[14000:15000]
wave_x = np.arange(wave_y.size)

t = wave_x
original = wave_y

processed = np.copy(original)

intensity = 4.0
last_v = processed[0]

for n in range(processed.size):
    v = processed[n]

    v1 = v + (v - last_v) * intensity

    v2 = 0.0
    if n < processed.size - 1:
        v2 = v + (v - processed[n + 1]) * intensity
    else:
        # the correct thing to do would be to take the first element of the
        # next buffer and do the same as above. This is done in our plugin code
        v2 = v + (last_v - v) * intensity

    processed[n] = 0.5 * (v1 + v2)

    last_v = v


peak_original = np.amax(np.fabs(original))
peak_processed = np.amax(np.fabs(processed))
rms_original = np.sqrt(np.mean(original * original))
rms_processed = np.sqrt(np.mean(processed * processed))
crest_original = 20 * np.log10(peak_original / rms_original)
crest_processsed = 20 * np.log10(peak_processed / rms_processed)

print("peak original:", peak_original)
print("rms original:", rms_original)
print("crest factor original:", crest_original)
print("peak processed:", peak_processed)
print("rms processed:", rms_processed)
print("crest factor processed:", crest_processsed)

fig = plt.figure()

plt.plot(t, original, 'bo-', markersize=4, label='original')
plt.plot(t, processed, 'ro-', markersize=4, label='processed')

fig.legend()

plt.xlabel('Arbitrary Time', fontsize=18)
plt.ylabel('Waveform', fontsize=18)
plt.grid()

plt.show()
