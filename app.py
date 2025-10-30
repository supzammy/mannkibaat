import streamlit as st
from preprocessing import preprocess_text
from model.inference import load_model, predict_risk, fallback_predict
from utils import map_score_to_risk, get_helpline_info


def _ensure_session_state():
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""


st.set_page_config(page_title="MannKiBaat — AI Screener", layout="centered")
_ensure_session_state()

st.title("MannKiBaat AI Mental Health Screener")

st.markdown(
    """
    This tool gives a quick, non-clinical screening based on short free-text responses.
    It is inspired by the attached guidance and resources. This is NOT a diagnosis.

    If you are in immediate danger, please contact local emergency services or the helpline shown for High risk.
    """
)

st.markdown("**Privacy note:** Your text is processed locally in memory. No data is sent anywhere by this demo.")

# Examples area: store input in session state for easier replacement
with st.expander("Try example responses"):
    col1, col2, col3 = st.columns(3)
    if col1.button("I'm feeling hopeless and alone"):
        st.session_state.user_input = "I'm feeling hopeless and alone"
    if col2.button("I feel anxious but I can manage"):
        st.session_state.user_input = "I feel anxious but I can manage"
    if col3.button("I don't want to live anymore"):
        st.session_state.user_input = "I don't want to live anymore"

# Main input area bound to session state so examples populate it
user_input = st.text_area("Enter how you feel in your own words:", key="user_input", height=160)

# Consent / disclaimer checkbox (inspired by the PDF's focus on safe usage)
consent = st.checkbox(
    "I understand this is an automated, non-clinical screener and not a medical diagnosis."
)

if st.button("Check Mental Health Risk"):
    if not consent:
        st.info("Please confirm you understand that this is not a clinical diagnosis by checking the box.")
    elif user_input.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        processed_text = preprocess_text(user_input)
        # Try to load the fine-tuned model; if missing, use a conservative heuristic fallback
        try:
            model = load_model()
            score = predict_risk(model, processed_text)
        except Exception as exc:  # keep broad exception here so the UI remains usable
            st.warning(
                "Fine-tuned model not available or failed to load — using a safe heuristic fallback."
            )
            score = fallback_predict(processed_text)

        risk_level = map_score_to_risk(score)
        st.write(f"**Risk Level:** {risk_level}")
        st.write(f"**Confidence:** {score:.2f}")
        helpline = get_helpline_info(risk_level)
        st.markdown(f"**Recommended Resources:** {helpline}")

        # Provide actionable next-steps inspired by guidance in the attached PDF
        if risk_level == "High":
            st.error(
                "If you're feeling like you might harm yourself or someone else, contact local emergency services immediately."
            )
        else:
            st.success("Consider reaching out to a trusted person, counselor, or a local helpline for support.")

        st.markdown(
            "---\n" "If you want the app to use your fine-tuned model, place your model files (e.g. `pytorch_model.bin`, `config.json`) in `model/fine_tuned_model/` and restart the app."
        )
