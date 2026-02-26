import streamlit as st
import qrcode
import uuid
import requests
import io
from twilio.rest import Client

# --------------------------------------------
# PAGE CONFIG
# --------------------------------------------
st.set_page_config(
    page_title="CityScan AI",
    page_icon="🚗",
    layout="centered"
)

# --------------------------------------------
# CLEAN AI UI THEME
# --------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
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
st.caption("Smart Secure Parking Identity System")

# --------------------------------------------
# HUGGINGFACE CONFIG
# --------------------------------------------
API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
HF_TOKEN = st.secrets.get("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")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
} if HF_TOKEN else None


def detect_face(image_bytes):
    if not headers:
        return {"error": "HF_TOKEN not configured"}
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.json()


# --------------------------------------------
# REGISTRATION CARD
# --------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("Register Vehicle")

name = st.text_input("Driver Name")
phone = st.text_input("Phone Number")
plate = st.text_input("Car Plate Number")
uploaded_image = st.file_uploader("Upload Face Image", type=["jpg", "png"])

generate = st.button("Generate Secure QR")

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------
# QR GENERATION
# --------------------------------------------
if generate:
    if not name or not phone or not plate:
        st.error("Please fill all fields.")
    else:
        unique_id = str(uuid.uuid4())[:8]

        # Detect face if uploaded
        if uploaded_image and headers:
            result = detect_face(uploaded_image.read())
            st.success("Face processed with AI.")
        elif uploaded_image and not headers:
            st.warning("HF_TOKEN not configured. Skipping AI.")

        # IMPORTANT: Replace with your real deployed URL
        APP_URL = "https://your-app-name.streamlit.app"

        qr_link = f"{APP_URL}?id={unique_id}"

        qr = qrcode.make(qr_link)
        buf = io.BytesIO()
        qr.save(buf)
        buf.seek(0)

        st.success("Registration Successful!")
        st.image(buf, caption="Scan this QR to Contact Driver")

        st.code(f"Secure ID: {unique_id}")

# --------------------------------------------
# CALL SECTION (READY FOR TWILIO)
# --------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("Call Driver (Demo Mode)")

if st.button("Call Driver Securely"):
    st.info("Calling driver...")
    st.success("This is demo mode. Integrate Twilio for real calling.")

st.markdown("</div>", unsafe_allow_html=True)
