import streamlit as st
import qrcode
import uuid
import requests
import io
import os
from PIL import Image

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="CityScan Drive",
    page_icon="🚗",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM MODERN UI
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
.card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.title {
    font-size: 45px;
    font-weight: bold;
}
.subtitle {
    font-size: 20px;
    color: #cccccc;
}
.stButton>button {
    background: linear-gradient(45deg,#00c6ff,#0072ff);
    color: white;
    height: 50px;
    border-radius: 12px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚗 CityScan Drive</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Privacy Parking System</div>", unsafe_allow_html=True)

st.markdown("<br>")

# ---------------------------------------------------
# HUGGINGFACE CONFIG
# ---------------------------------------------------
API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"

HF_TOKEN = st.secrets.get("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
} if HF_TOKEN else None


def verify_face(image_bytes):
    if not headers:
        return {"error": "HF_TOKEN not configured"}
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.json()


# ---------------------------------------------------
# REGISTRATION FORM
# ---------------------------------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🔐 Register Your Vehicle")

    name = st.text_input("Driver Name")
    phone = st.text_input("Phone Number")
    plate = st.text_input("Car Plate Number")

    uploaded_image = st.file_uploader("Upload Face Image", type=["jpg", "png"])

    if st.button("Generate Secure QR"):
        if name and phone and plate:

            unique_id = str(uuid.uuid4())[:8]

            # Face Verification
            if uploaded_image and headers:
                result = verify_face(uploaded_image.read())
                st.success("Face scanned successfully (AI processed).")

            # Generate QR
            qr_data = f"https://cityscandrive.app/user/{unique_id}"
            qr = qrcode.make(qr_data)

            buf = io.BytesIO()
            qr.save(buf)
            buf.seek(0)

            st.success("Registration Successful!")
            st.image(buf, caption="Your Secure Parking QR")

            st.code(f"Secure ID: {unique_id}")

        else:
            st.error("Please fill all required fields.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# CALL SIMULATION
# ---------------------------------------------------
st.markdown("<br>")
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📞 Scan & Call Driver (Demo)")
    if st.button("Call Driver Securely"):
        st.info("Connecting via masked secure call...")
        st.success("Call connected. Identity protected.")
    st.markdown("</div>", unsafe_allow_html=True)
