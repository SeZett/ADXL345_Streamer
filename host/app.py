import streamlit as st
import serial
import struct
import time
import pandas as pd
from collections import deque

# ---------------------- Frame Definition ----------------------
FRAME_SIZE = 10
FRAME_STRUCT = struct.Struct("<Ihhh")

# ---------------------- Session State ----------------------
if "recorded_frames" not in st.session_state:
    st.session_state.recorded_frames = []

if "data_queue" not in st.session_state:
    st.session_state.data_queue = deque(maxlen=1000)

# ---------------------- Streamlit UI ----------------------
st.title("ADXL345 Live Stream (RP2040)")

# Port Eingabe
port = st.text_input("Serial Port", value="/dev/ttyACM0")
frames_to_read = st.number_input("Anzahl Frames zum Lesen", min_value=1, value=100)

# ---------------------- Lesen ----------------------
if st.button("Starte Lesen"):
    try:
        ser = serial.Serial(port, 2000000, timeout=1)
        st.write("Port geöffnet, warte 2 Sekunden für RP2040 Reset...")
        time.sleep(2)

        for i in range(frames_to_read):
            raw = ser.read(FRAME_SIZE)
            if len(raw) == FRAME_SIZE:
                ts, x, y, z = FRAME_STRUCT.unpack(raw)
                frame = {"timestamp_us": ts, "x": x, "y": y, "z": z}
                st.session_state.recorded_frames.append(frame)
                st.session_state.data_queue.append(frame)
            else:
                st.warning(f"Frame {i+1}: nicht vollständig empfangen")

        ser.close()
        st.success("Port geschlossen, Lesen beendet")

    except Exception as e:
        st.error(str(e))

# ---------------------- Live-Plot ----------------------
if st.session_state.data_queue:
    df_live = pd.DataFrame(list(st.session_state.data_queue))
    st.line_chart(df_live.set_index("timestamp_us"))

# ---------------------- CSV Export ----------------------
if st.button("Export CSV"):
    if st.session_state.recorded_frames:
        df = pd.DataFrame(st.session_state.recorded_frames)
        df.to_csv("adxl_record.csv", index=False)
        st.success(f"{len(st.session_state.recorded_frames)} Frames gespeichert → adxl_record.csv")
    else:
        st.warning("Keine Daten vorhanden")
