import textwrap
import streamlit as st


def footer_home():
    st.markdown(
        textwrap.dedent("""
        <div class="snap-footer-home">
            <p class="snap-footer-text">
                Created with ❤️ by <span class="snap-footer-author">Parshuram Prajapati</span>
            </p>
        </div>
        """),
        unsafe_allow_html=True,
    )


def footer_dashboard():
    st.markdown(
        textwrap.dedent("""
        <div class="snap-footer-dashboard">
            <p class="snap-footer-dashboard-text">
                Created with ❤️ by <span class="snap-footer-dashboard-author">Parshuram Prajapati</span>
            </p>
        </div>
        """),
        unsafe_allow_html=True,
    )
