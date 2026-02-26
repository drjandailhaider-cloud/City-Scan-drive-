import streamlit as st
import qrcode
import uuid
import requests
from PIL import Image
import io
import base64

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="SmartPark Privacy",
    page_icon="🚗",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS (Beautiful UI)
# ------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
}
.stApp {
    background: transparent;
}
.card {
    background: rgba(255,255,255,0.1);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37);
}
.big-title {
    font-size:40px;
    font-weight:bold;
    color:white;
}
.sub-text {
    color:lightgray;
}
.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------
st.markdown("<div class='big-title'>🚗 SmartPark Privacy</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Generate Secure QR for Your Car</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------
# DRIVER FORM
# ------------------------------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    name = st.text_input("Driver Name")
    phone = st.text_input("Phone Number")
    car_plate = st.text_input("Car Plate Number")

    uploaded_face = st.file_uploader("Upload Face Image", type=["jpg", "png"])

    if st.button("🔐 Register & Generate QR"):
        if name and phone and car_plate:
            unique_id = str(uuid.uuid4())[:8]

            # Generate QR
            qr_data = f"https://smartpark.app/user/{unique_id}"
            qr = qrcode.make(qr_data)

            buffer = io.BytesIO()
            qr.save(buffer)
            buffer.seek(0)

            st.success("Registration Successful!")
            st.image(buffer, caption="Your Secure Parking QR")

            st.markdown(f"""
            ### 🔑 Your Secure ID:
            `{unique_id}`
            """)

        else:
            st.error("Please fill all required fields.")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# CALL DRIVER SECTION (SIMULATION)
# ------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("### 📞 Scan QR & Call Driver (Demo)")

if st.button("Call Driver"):
    st.info("Connecting via Secure Masked Call...")
    st.success("Call Connected (Number Hidden)")

st.markdown("</div>", unsafe_allow_html=True)
