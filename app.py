import streamlit as st
import qrcode
import uuid
import io
import json
import os
from twilio.rest import Client

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="CityScan AI", page_icon="🚗")

DATA_FILE = "drivers.json"

# --------------------------------------------------
# LOAD DATABASE
# --------------------------------------------------
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

with open(DATA_FILE, "r") as f:
    drivers = json.load(f)

# --------------------------------------------------
# TWILIO CONFIG
# --------------------------------------------------
TWILIO_SID = st.secrets.get("TWILIO_SID")
TWILIO_AUTH = st.secrets.get("TWILIO_AUTH")
TWILIO_NUMBER = st.secrets.get("TWILIO_NUMBER")

def call_driver(phone):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    call = client.calls.create(
        to=phone,
        from_=TWILIO_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"
    )
    return call.sid

# --------------------------------------------------
# CHECK QR SCAN
# --------------------------------------------------
query_params = st.query_params
driver_id = query_params.get("id")

if driver_id:
    if driver_id in drivers:
        driver = drivers[driver_id]

        st.title("🚗 Vehicle Found")
        st.write("Plate:", driver["plate"])

        if st.button("📞 Call Driver"):
            try:
                sid = call_driver(driver["phone"])
                st.success("Calling driver...")
                st.write("Call SID:", sid)
            except Exception as e:
                st.error(f"Call failed: {e}")
    else:
        st.error("Driver not found.")

    st.stop()

# --------------------------------------------------
# REGISTRATION
# --------------------------------------------------
st.title("🚗 CityScan AI")
st.subheader("Register Your Vehicle")

name = st.text_input("Driver Name")
phone = st.text_input("Phone (+country code)")
plate = st.text_input("Car Plate Number")

if st.button("Generate QR"):
    if not name or not phone or not plate:
        st.error("Fill all fields")
    else:
        unique_id = str(uuid.uuid4())[:8]

        drivers[unique_id] = {
            "name": name,
            "phone": phone,
            "plate": plate
        }

        with open(DATA_FILE, "w") as f:
            json.dump(drivers, f)

        APP_URL = "https://YOUR_STREAMLIT_APP.streamlit.app"

        qr_link = f"{APP_URL}?id={unique_id}"

        qr = qrcode.make(qr_link)
        buf = io.BytesIO()
        qr.save(buf)
        buf.seek(0)

        st.success("QR Generated Successfully")
        st.image(buf)
        st.code(qr_link)
