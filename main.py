import sys

import numpy as np
import wave
import struct
from tqdm import tqdm

morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',

    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',

    '.': '.-.-.-', ':': '---...', ',': '--..--', ';': '-.-.-.', '?': '..--..',
    '=': '-...-', '\'': '.----.', '/': '-..-.', '!': '-.-.--', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '(': '-.--.', ')': '-.--.-', '$': '...-..-',
    '&': '.-...', '@': '.--.-.'
}

plain_text = str.upper(sys.argv[1])

morse_arr = []
for text in plain_text:
    morse_arr.append(morse_dict[text])
morse_text = "/".join(morse_arr)
print("morse text: " + morse_text)

# frequency is the number of times a wave repeats a second
frequency = 1000
num_samples = int(1000 / len(plain_text)) * 50
print("num samples: " + str(num_samples))

# The sampling rate of the analog to digital convert
sampling_rate = 48000.0
amplitude = 16000

morse_wave_Dit = [np.sin(2 * np.pi * frequency * x/sampling_rate) for x in range(num_samples)]
morse_wave_Dah = [np.sin(2 * np.pi * frequency * x/sampling_rate) for x in range(num_samples * 3)]
morse_null_short = [0 for x in range(num_samples)]
morse_null_long = [0 for x in range(num_samples * 3)]

morse_wave = []
for morse in morse_text:
    match morse:
        case ".":
            morse_wave.extend(morse_wave_Dit)
            morse_wave.extend(morse_null_short)
        case "-":
            morse_wave.extend(morse_wave_Dah)
            morse_wave.extend(morse_null_short)
        case "/":
            morse_wave.extend(morse_null_long)

n_frames = num_samples
wav_file = wave.open("output.wav", 'w')
wav_file.setparams((1, 2, int(sampling_rate), n_frames, "NONE", "not compressed"))
pbar = tqdm(morse_wave, desc="Writing Morse Audio")
for s in pbar:
    wav_file.writeframes(struct.pack('h', int(s * amplitude)))
