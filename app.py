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
    /* DESKTOP BACKGROUND */
    .stApp {{
        background:
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
            url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* MOBILE: REMOVE BACKGROUND IMAGE */
    @media (max-width: 768px) {{
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92));
        }}
    }}

    html, body {{
        overflow-x: hidden;
    }}
    </style>
    """, unsafe_allow_html=True)

    return encoded

bg_encoded = add_bg("cyber.jpg")

# =================================================
# =============== WELCOME PAGE ====================
# =================================================
def welcome_page():
    st.markdown("""
    <style>
    .welcome-box {
        min-height: 100svh;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        color: white;
        padding: 1rem;
    }

    .welcome-box h1 {
        font-size: 64px;
        margin-bottom: 18px;
    }

    .welcome-box p {
        font-size: 22px;
        opacity: 0.9;
        margin-bottom: 30px;
    }

    /* MOBILE LOCK IMAGE */
    .mobile-lock {
        display: none;
    }

    @media (max-width: 768px) {
        .welcome-box h1 {
            font-size: 36px;
        }

        .welcome-box p {
            font-size: 16px;
        }

        .mobile-lock {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }

        .mobile-lock img {
            width: 85%;
            max-width: 320px;
            opacity: 0.9;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="welcome-box">
        <h1>🛡️ X-MailGuard</h1>
        <p>
        Multilingual Email Threat Detection System<br>
        English • Telugu • French
        </p>

        <!-- MOBILE FULL LOCK IMAGE -->
        <div class="mobile-lock">
            <img src="data:image/jpg;base64,{bg_encoded}" alt="Security Lock">
        </div>
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

    tfidf = joblib.load("models/tfidf.pkl")
    model = joblib.load("models/rf_model.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")

    st.markdown("""
    <style>
    label, h3, p, li {
        color: #eaf2ff !important;
    }

    .block-container {
        padding: 2.5rem 4rem;
        max-width: 100%;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.2rem 1rem;
        }
    }

    .header {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 48px;
        border-radius: 26px;
        text-align: center;
        color: white;
        margin-bottom: 45px;
    }

    .card {
        background: rgba(12, 20, 30, 0.94);
        padding: 34px;
        border-radius: 22px;
        margin-bottom: 30px;
    }

    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

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
        email_text = st.text_area("📧 Email Content", height=260)
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

    if analyze and email_text.strip():
        clean = preprocess(email_text)
        X = tfidf.transform([clean])
        pred = model.predict(X)[0]
        label = label_encoder.inverse_transform([pred])[0]
        confidence = max(model.predict_proba(X)[0])

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            "✅ SAFE EMAIL" if label.lower() == "safe" else f"🚨 {label.upper()}",
            unsafe_allow_html=True
        )
        st.markdown(f"Confidence: {confidence:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# =============== ROUTER ==========================
# =================================================
if st.session_state.page == "welcome":
    welcome_page()
else:
    main_app()
