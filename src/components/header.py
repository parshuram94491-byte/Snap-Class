import textwrap
import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(
        textwrap.dedent(f"""
        <div class="snap-brand-header">
            <div class="snap-brand-logo-badge">
                <svg class="snap-logo-fallback" viewBox="0 0 64 64" role="img" aria-label="SnapClass graduation cap">
                    <path d="M7 23 32 12l25 11-25 11L7 23Z" fill="#fff" stroke="#1D2A55" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M17 28v13c8 7 22 7 30 0V28" fill="#fff" stroke="#1D2A55" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M56 23v15" stroke="#1D2A55" stroke-width="2.5" stroke-linecap="round"/>
                    <circle cx="56" cy="41" r="3" fill="#EC369B"/>
                    <path d="M22 48h20l5 5v3H17v-3l5-5Z" fill="#fff" stroke="#1D2A55" stroke-width="2.5" stroke-linejoin="round"/>
                </svg>
                <img src="{logo_url}" alt="SnapClass Logo" onerror="this.style.display='none'" />
            </div>
            <h1 class="snap-brand-wordmark">
                <span class="word-snap">SNAP</span>
                <span class="word-class">CLASS</span>
            </h1>
            <p class="snap-brand-tagline">Smart Attendance. Smarter Classrooms.</p>
            <div class="snap-brand-indicator">
                <span class="snap-pill"></span>
                <span class="snap-dot"></span>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def header_dashboard():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px">
            <img src='{logo_url}' style='height:85px;' />
            <h2 style='text-align:left; color:#4F5FF5'>SNAP<br/>CLASS</h2>
        </div>   
                
                """, unsafe_allow_html=True)
