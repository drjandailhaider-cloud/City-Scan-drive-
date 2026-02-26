import streamlit as st
import qrcode
import uuid
import io
from twilio.rest import Client

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="CityScan AI",
    page_icon="🚗",
    layout="centered"
)

# --------------------------------------------------
# CLEAN PROFESSIONAL UI
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1 {
    color: #00e0ff;
}
.stTextInput>div>div>input {
    background-color: #1c1f26;
    color: white;
    border-radius: 8px;
}
.stButton>button {
    background-color: #00e0ff;
    color: black;
    border-radius: 8px;
    height: 45px;
    font-weight: bold;
}
.card {
    background-color: #161b22;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚗 CityScan AI")
st.caption("Secure Smart Parking Contact System")

# --------------------------------------------------
# TWILIO CONFIG (FROM SECRETS)
# --------------------------------------------------
TWILIO_SID = st.secrets.get("TWILIO_SID")
TWILIO_AUTH = st.secrets.get("TWILIO_AUTH")
TWILIO_NUMBER = st.secrets.get("TWILIO_NUMBER")

def call_driver(driver_phone):
    client = Client(TWILIO_SID, TWILIO_AUTH)

    call = client.calls.create(
        to=driver_phone,
        from_=TWILIO_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"
    )

    return call.sid

# --------------------------------------------------
# SESSION STORAGE (TEMP DATABASE)
# --------------------------------------------------
if "drivers" not in st.session_state:
    st.session_state.drivers = {}

# --------------------------------------------------
# CHECK IF QR LINK OPENED
# --------------------------------------------------
query_params = st.query_params
scanned_id = query_params.get("id")

if scanned_id:
    driver = st.session_state.drivers.get(scanned_id)

    if driver:
        st.success("Driver Found")
        st.write("Car Plate:", driver["plate"])

        if st.button("📞 Call Driver Securely"):
            try:
                call_sid = call_driver(driver["phone"])
                st.success("Calling driver...")
                st.write("Call SID:", call_sid)
            except Exception as e:
                st.error(f"Call Failed: {e}")
    else:
        st.error("Driver not found.")

    st.stop()

# --------------------------------------------------
# REGISTRATION SECTION
# --------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("Register Your Vehicle")

name = st.text_input("Driver Name")
phone = st.text_input("Phone Number (with country code, e.g. +923001234567)")
plate = st.text_input("Car Plate Number")

generate = st.button("Generate Secure QR")

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# QR GENERATION
# --------------------------------------------------
if generate:
    if not name or not phone or not plate:
        st.error("Please fill all fields.")
    else:
        unique_id = str(uuid.uuid4())[:8]

        # Store in session (temporary DB)
        st.session_state.drivers[unique_id] = {
            "name": name,
            "phone": phone,
            "plate": plate
        }

        # IMPORTANT: Replace after deployment
        APP_URL = "https://YOUR_STREAMLIT_URL.streamlit.app"

        qr_link = f"{APP_URL}?id={unique_id}"

        qr = qrcode.make(qr_link)
        buf = io.BytesIO()
        qr.save(buf)
        buf.seek(0)

        st.success("Registration Successful!")
        st.image(buf, caption="Scan this QR to Call Driver")

        st.code(f"Secure ID: {unique_id}")

        st.info("Print and place this QR inside your car.")
