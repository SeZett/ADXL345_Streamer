#!/usr/bin/env python3
import serial
import struct
import csv
import time
import argparse

# ---------------------- Kommandozeilen-Argumente ----------------------
parser = argparse.ArgumentParser(description="ADXL345 RP2040 Binary Recorder")
parser.add_argument("--port", required=True, help="Serial port (z.B. /dev/ttyACM0 oder COM5)")
parser.add_argument("--rate", type=int, default=1000, help="Sampling rate [Hz] (1-3200)")
parser.add_argument("--duration", type=float, default=10.0, help="Recording duration [s]")
parser.add_argument("--out", default="data.csv", help="CSV output file")
args = parser.parse_args()

# ---------------------- Frame Definition ----------------------
# Firmware sendet:
# struct __attribute__((packed)) Frame {
#     uint32_t timestamp_us;
#     int16_t x, y, z;
# };
FRAME_SIZE = 10  # 4 + 2 + 2 + 2
FRAME_STRUCT = struct.Struct("<Ihhh")  # Little-endian

# ---------------------- Serial Setup ----------------------
ser = serial.Serial(args.port, 2000000, timeout=1)
time.sleep(2)  # Warte, bis Pico bereit ist

# ---------------------- Set Rate ----------------------
ser.write(f"SET_RATE {args.rate}\n".encode("ascii"))
time.sleep(0.1)

# ---------------------- Start Recording ----------------------
ser.write(b"START\n")
print(f"Recording {args.duration}s at {args.rate}Hz...")

start_time = time.time()
frames_received = 0

with open(args.out, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["timestamp_us", "x", "y", "z"])  # Header

    while (time.time() - start_time) < args.duration:
        raw = ser.read(FRAME_SIZE)
        if len(raw) != FRAME_SIZE:
            continue
        timestamp_us, x, y, z = FRAME_STRUCT.unpack(raw)
        writer.writerow([timestamp_us, x, y, z])
        frames_received += 1

# ---------------------- Stop ----------------------
ser.write(b"STOP\n")
ser.close()
print(f"Recording finished, {frames_received} frames saved to {args.out}")
