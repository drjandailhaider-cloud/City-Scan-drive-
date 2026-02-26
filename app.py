import streamlit as st
import qrcode
import uuid
import io
from twilio.rest import Client
import urllib.parse

st.set_page_config(page_title="CityScan AI", page_icon="🚗")

st.title("🚗 CityScan AI")
st.caption("Secure Parking Contact System")

# ---------------- TWILIO CONFIG ----------------
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

# ---------------- CHECK QR OPEN ----------------
query_params = st.query_params

phone_from_url = query_params.get("phone")
plate_from_url = query_params.get("plate")

if phone_from_url:
    st.success("Vehicle Found")
    st.write("Plate:", plate_from_url)

    if st.button("📞 Call Driver"):
        try:
            sid = call_driver(phone_from_url)
            st.success("Calling driver...")
            st.write("Call SID:", sid)
        except Exception as e:
            st.error(f"Call failed: {e}")

    st.stop()

# ---------------- REGISTRATION ----------------
st.subheader("Register Vehicle")

name = st.text_input("Driver Name")
phone = st.text_input("Phone (+country code)")
plate = st.text_input("Car Plate Number")

if st.button("Generate QR"):
    if not phone or not plate:
        st.error("Fill all fields")
    else:
        APP_URL = "https://gzv6rzmomvmidvgqk7azpn.streamlit.app"

        encoded_phone = urllib.parse.quote(phone)
        encoded_plate = urllib.parse.quote(plate)

        qr_link = f"{APP_URL}?phone={encoded_phone}&plate={encoded_plate}"

        qr = qrcode.make(qr_link)
        buf = io.BytesIO()
        qr.save(buf)
        buf.seek(0)

        st.success("QR Generated Successfully")
        st.image(buf)
        st.code(qr_link)
