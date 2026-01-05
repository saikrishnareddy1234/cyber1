import streamlit as st
import joblib
import base64
from nlp.preprocess import preprocess

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="X-MailGuard",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# ---------------- BACKGROUND IMAGE ----------------
def add_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background:
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
            url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

add_bg("cyber1.jpg")

# =================================================
# =============== WELCOME PAGE ====================
# =================================================
def welcome_page():
    st.markdown("""
    <style>
    .welcome-box {
        height: 80vh;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        color: white;
    }

    .welcome-box h1 {
        font-size: 64px;
        margin-bottom: 18px;
    }

    .welcome-box p {
        font-size: 22px;
        opacity: 0.9;
        margin-bottom: 45px;
    }

    .welcome-btn button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        border-radius: 20px;
        padding: 18px 46px;
        font-size: 22px;
        font-weight: 600;
        box-shadow: 0 20px 45px rgba(0,160,255,0.6);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .welcome-btn button:hover {
        transform: translateY(-4px);
        box-shadow: 0 28px 60px rgba(0,180,255,0.85);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-box">
        <h1>🛡️ X-MailGuard</h1>
        <p>
        Multilingual Email Threat Detection System<br>
        English • Telugu • French
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Let's Go", use_container_width=True):
            st.session_state.page = "app"
            st.rerun()

# =================================================
# =============== MAIN APP PAGE ===================
# =================================================
def main_app():

    # LOAD MODELS
    tfidf = joblib.load("models/tfidf.pkl")
    model = joblib.load("models/rf_model.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")

    # ---------------- GLOBAL CSS ----------------
    st.markdown("""
    <style>

    label, h3, p, li {
        color: #eaf2ff !important;
    }

    .block-container {
        padding: 2.5rem 6rem;
    }

    .header {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 48px;
        border-radius: 26px;
        text-align: center;
        color: white;
        box-shadow: 0 18px 50px rgba(0,0,0,0.85);
        margin-bottom: 45px;
    }

    .card {
        background: rgba(12, 20, 30, 0.94);
        backdrop-filter: blur(18px);
        padding: 34px;
        border-radius: 22px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        margin-bottom: 30px;
    }

    div[data-testid="InputInstructions"] {
        display: none !important;
    }

    /* TEXTAREA */
    div[data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        color: #000000 !important;
        border-radius: 14px !important;
        border: 1.8px solid #d0d7e2 !important;
        padding: 20px !important;
        font-size: 16px !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    div[data-testid="stTextArea"] textarea:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }

    div[data-testid="stTextArea"] textarea:focus {
        outline: none !important;
        border-color: #00b4ff !important;
        box-shadow: 0 14px 36px rgba(0,140,255,0.45);
    }

    /* BUTTON */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        border-radius: 14px;
        height: 3.3em;
        font-size: 18px;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.25s ease;
    }

    button[kind="primary"]:hover {
        box-shadow: 0 12px 30px rgba(0,150,255,0.55);
        transform: translateY(-2px);
    }

    /* RESULTS */
    .result-safe {
        background: linear-gradient(90deg, rgba(46,204,113,0.35), rgba(46,204,113,0.15));
        border-left: 8px solid #2ecc71;
        padding: 20px 26px;
        border-radius: 18px;
        font-size: 22px;
        font-weight: 700;
        color: #d9ffe9;
        box-shadow:none;
    }

    .result-danger {
        background: linear-gradient(90deg, rgba(231,76,60,0.35), rgba(231,76,60,0.15));
        border-left: 8px solid #e74c3c;
        padding: 20px 26px;
        border-radius: 18px;
        font-size: 22px;
        font-weight: 700;
        color: #ffd7d2;
        box-shadow:none;
    }

    .result-confidence {
        margin-top: 14px;
        background: rgba(0,114,255,0.22);
        padding: 14px 20px;
        border-radius: 14px;
        font-size: 18px;
        color: #e3efff;
    }

    footer { visibility: hidden; }

    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("""
    <div class="header">
        <h1>🛡️ X-MailGuard</h1>
        <p>
        Multilingual Email Threat Detection System<br>
        <small>English • Telugu • French</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([2.3, 1])

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        email_text = st.text_area(
            "📧 Email Content",
            height=260,
            placeholder="Paste the email content here for security analysis..."
        )
        analyze = st.button("🔍 Analyze Email", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔐 How It Works")
        st.markdown("""
        • Text preprocessing  
        • TF-IDF feature extraction  
        • Random Forest classification  
        • Multilingual detection  
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    if analyze:
        if email_text.strip() == "":
            st.warning("⚠️ Please enter an email to analyze.")
        else:
            clean = preprocess(email_text)
            X = tfidf.transform([clean])
            pred = model.predict(X)[0]
            label = label_encoder.inverse_transform([pred])[0]
            confidence = max(model.predict_proba(X)[0])

            st.markdown('<div class="card">', unsafe_allow_html=True)

            if label.lower() == "safe":
                st.markdown('<div class="result-safe">✅ SAFE EMAIL</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-danger">🚨 {label.upper()}</div>', unsafe_allow_html=True)

            st.markdown(
                f'<div class="result-confidence">📊 Confidence Score: <b>{confidence:.2f}</b></div>',
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:center; color:#bbb; margin-top:40px;">
    X-MailGuard © 2026 | National-Level Cybersecurity Project
    </p>
    """, unsafe_allow_html=True)

# =================================================
# =============== PAGE ROUTER =====================
# =================================================
if st.session_state.page == "welcome":
    welcome_page()
else:
    main_app()
