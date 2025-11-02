"""
MannKiBaat - AI Mental Health Screener
Main Streamlit application interface.
"""

import streamlit as st
from model import get_risk_assessment
from utils import map_score_to_risk, format_result_message


# Page configuration
st.set_page_config(
    page_title="MannKiBaat - AI Mental Health Screener",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# Custom CSS for professional styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .privacy-note {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1.5rem 0;
    }
    .example-box {
        background-color: #e8f4f8;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .disclaimer {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Header
st.markdown(
    '<div class="main-header">🧠 MannKiBaat - AI Mental Health Screener</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">A safe, anonymous tool for mental health awareness</div>',
    unsafe_allow_html=True,
)


# Introduction
st.markdown(
    """
This tool provides a quick, non-clinical screening based on your written responses. 
It's designed to help identify potential mental health concerns and connect you with appropriate resources.

**This is NOT a medical diagnosis.** If you are in immediate danger, please contact emergency services.
"""
)


# Privacy Notice
st.markdown(
    """
<div class="privacy-note">
    <strong>🔒 Your Privacy Matters</strong><br>
    Your text is processed locally and is <strong>not stored or shared</strong> with anyone. 
    This tool respects your anonymity and confidentiality.
</div>
""",
    unsafe_allow_html=True,
)


# Example inputs section
with st.expander("💡 See Example Responses", expanded=False):
    st.markdown(
        """
    <div class="example-box">
    <strong>Examples of what you can share:</strong>
    <ul>
        <li>"I feel exhausted all the time and can't focus on anything"</li>
        <li>"I feel worthless and like nothing I do matters"</li>
        <li>"I'm constantly worried and having panic attacks"</li>
        <li>"I feel hopeless and alone, like there's no point anymore"</li>
    </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )


# Main input area
st.markdown("### Share How You've Been Feeling")
user_input = st.text_area(
    label="Your Response",
    placeholder="Share how you've been feeling (e.g., I feel exhausted, worthless, can't focus)...",
    height=150,
    help="Be as honest and detailed as you're comfortable with. Your input helps us provide better guidance.",
    label_visibility="collapsed",
)


# Consent checkbox
consent = st.checkbox(
    "I understand this is an automated screening tool and not a medical diagnosis",
    help="This tool provides guidance only. For medical advice, please consult a healthcare professional.",
)


# Submit button
if st.button("🔍 Analyze My Mental Health", type="primary", use_container_width=True):
    if not consent:
        st.info(
            "✋ Please confirm you understand this is not a clinical diagnosis by checking the box above."
        )
    elif not user_input or len(user_input.strip()) < 10:
        st.warning(
            "⚠️ Please enter a more detailed response (at least 10 characters) so we can provide a meaningful assessment."
        )
    else:
        # Show processing spinner
        with st.spinner("Analyzing your response..."):
            try:
                # Get risk assessment
                score, used_fallback = get_risk_assessment(user_input)
                risk_level = map_score_to_risk(score)
                result = format_result_message(risk_level, score, used_fallback)

                # Display results
                st.markdown("---")
                st.markdown("### 📊 Assessment Results")

                # Risk level display with color coding
                if risk_level == "High":
                    st.error(f"**Risk Level:** {risk_level}")
                elif risk_level == "Medium":
                    st.warning(f"**Risk Level:** {risk_level}")
                else:
                    st.success(f"**Risk Level:** {risk_level}")

                # Confidence score
                st.metric("Confidence Score", f"{score:.2%}")

                # Model info (if fallback was used)
                if used_fallback:
                    st.info(
                        "ℹ️ Note: Using heuristic analysis (fine-tuned model not available)"
                    )

                # Helpline information
                st.markdown("### 📞 Recommended Resources")
                st.info(result["helpline"])

                # Warning for high risk
                if result["warning"]:
                    st.error(result["warning"])

                # Additional guidance
                if risk_level != "High":
                    st.success(
                        "💚 Consider reaching out to a trusted person, counselor, or local helpline for support."
                    )

            except Exception as e:
                st.error(f"❌ An error occurred during analysis: {str(e)}")
                st.info("Please try again or contact support if the issue persists.")


# Disclaimer at bottom
st.markdown("---")
st.markdown(
    """
<div class="disclaimer">
    <strong>⚠️ Important Disclaimer</strong><br>
    This tool is for educational and awareness purposes only. It does not replace professional 
    mental health evaluation or treatment. If you're experiencing a mental health crisis, 
    please contact your local emergency services or a mental health crisis helpline immediately.
</div>
""",
    unsafe_allow_html=True,
)


# Footer
st.markdown(
    """
<div style="text-align: center; color: #888; margin-top: 2rem; font-size: 0.85rem;">
    MannKiBaat | Made with care for mental health awareness<br>
    <a href="https://github.com/supzammy/mannkibaat" target="_blank">View on GitHub</a>
</div>
""",
    unsafe_allow_html=True,
)
