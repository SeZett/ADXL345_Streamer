import serial
import time
import struct

FRAME_SIZE = 10  # 4 + 2 + 2 + 2
FRAME_STRUCT = struct.Struct("<Ihhh")

# Port öffnen
ser = serial.Serial("/dev/ttyACM0", 2000000, timeout=1)
print("Port geöffnet, warte 2 Sekunden für RP2040 Reset...")
time.sleep(2)  # Reset abwarten

# START senden
#ser.write(b"START\n")
#print("[TX] START gesendet")

# 5 Frames lesen
for i in range(5):
    raw = ser.read(FRAME_SIZE)
    if len(raw) == FRAME_SIZE:
        ts, x, y, z = FRAME_STRUCT.unpack(raw)
        print(f"Frame {i+1}: ts={ts}, x={x}, y={y}, z={z}")
    else:
        print(f"Frame {i+1}: nicht vollständig empfangen")

# STOP senden
#ser.write(b"STOP\n")
#print("[TX] STOP gesendet")

ser.close()
print("Port geschlossen")
