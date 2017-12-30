
import random
import sys
import time


with open("/home/nemesis/Downloads/top_secret_86d05414a795935dcdd0f8128f53baa7", "rb") as f:
    enc = list(f.read())
time = []
for i in enc[len(enc) - 18:len(enc)]:
    time.append(i ^ 0x88)
msg = enc[:len(enc) - 18]

random.seed(''.join([chr(i) for i in time]))

key = [random.randrange(256) for _ in msg]
c = [int(m) ^ int(k) for (m, k) in zip(msg + time, key + [0x88] * len(time))]

print(''.join([chr(i) for i in c]))
