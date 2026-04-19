import streamlit as st

def footer_home():
    st.markdown("""
    <style>

    .footer {
        position: fixed;
        bottom: 25px;
        width: 100%;
        display: flex;
        justify-content: center;
        z-index: 100;
    }

    .footer-box {
        padding: 10px 28px;
        border-radius: 30px;
        font-size: 16px;
        font-weight: 500;
        color: white;

        background: linear-gradient(
            135deg,
            rgba(255,255,255,0.25),
            rgba(255,255,255,0.05)
        );

        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.2);

        box-shadow:
            0 8px 25px rgba(0,0,0,0.15),
            inset 0 0 10px rgba(255,255,255,0.15);

        transition: all 0.3s ease;
    }

    .footer-box:hover{
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    }

    .heart{
        display:inline-block;
        animation: heartbeat 1.4s infinite;
        color:#ff4b4b;
    }

    @keyframes heartbeat{
        0%{transform:scale(1)}
        25%{transform:scale(1.2)}
        50%{transform:scale(1)}
        75%{transform:scale(1.2)}
        100%{transform:scale(1)}
    }

    .dev{
        font-weight:600;
        color:#ffffff;
    }

    </style>

    <div class="footer">
        <div class="footer-box">
            Built with <span class="heart">❤️</span> by 
            <span class="dev">Satinder Singh Sall</span>
        </div>
    </div>

    """, unsafe_allow_html=True)

footer_home()
