import wave, os, random, struct, math

length = 44100

sound = wave.open('generated.wav', 'w')

sound.setparams((1, 2, 44100, length, 'NONE', 'not compressed'))

for i in range(0, length):
    value = math.sin(i ** 2 / 3000) * 7000
    if value > 32767:
        value = 32767
    if value < -32767:
        value = -32767
    packed_value = struct.pack('h', int(value))
    sound.writeframes(packed_value)
