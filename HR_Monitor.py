import spidev
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque



spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000

def read_channel(channel):
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    return result

def convert_to_voltage(value, vref = 3.3):
    return (value * vref) / 1023

def moving_average(data, window=4):
    arr = np.array(data)
    if len(arr) < window:
        return arr
    return np.convolve(arr, np.ones(window)/window, mode='same')

samples = 500
vref = 3.3
data = deque([0] * samples, maxlen=samples)

fig, ax = plt.subplots()
line, = ax.plot(range(samples), data)
ax.set_ylim(0, vref)
ax.set_title("ECG")
ax.set_ylabel("V")
ax.set_xlabel("sample")
ax.grid(True)

def update(frame):
    raw = read_channel(0)
    voltage = convert_to_voltage(raw)
    data.append(voltage)
    smoothed = moving_average(data)
    line.set_ydata(smoothed)
    return line,

ani = animation.FuncAnimation(fig, update, interval=5, cache_frame_data= False)
plt.show()