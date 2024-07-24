import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg') # using tkinter for visualization <3

CHUNK = 1024 * 4  # 4096 samples per chunk
FORMAT = pyaudio.paInt16
CHANNELS = 1  # mono sound because only one mic
RATE = 44100 #standard rate 44.1 khz

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True, #initialize as true
    output=True, #initialize as true
    frames_per_buffer=CHUNK
)

# create the plot
fig, ax = plt.subplots()
plt.ion()  # interactive mode on
x = np.arange(0, 2 * CHUNK)  # x values should match the length of data_int
line, = ax.plot(x, np.random.rand(2 * CHUNK))

# set y-axis limits to fit 16-bit audio
ax.set_ylim(-2000, 2000)
ax.set_xlim(0, 2 * CHUNK)

# set plot labels and title
ax.set_title("Real-Time Audio Waveform")
ax.set_xlabel("Sample Index")
ax.set_ylabel("Amplitude")

try:
    while True:
        # read the audio data
        data = stream.read(CHUNK * 2)

        # unpack the data into 16-bit integers and center it around zero
        data_int = np.array(struct.unpack(str(2 * CHUNK) + 'h', data), dtype='int16')

        # update the line plot with new data
        line.set_ydata(data_int)

        # draw and flush the plot
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)  # Small pause to give GUI time to update
except KeyboardInterrupt:
    print("Stream stopped by user.")
    stream.stop_stream()
    stream.close()
    p.terminate()
