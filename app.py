"""
MannKiBaat - AI Mental Health Screener
Enhanced Streamlit application with PHQ-8 integration and cultural context.
"""

import streamlit as st
from phq8_model import analyze_depression_risk
from config import PHQ8_THRESHOLDS
from input_validator import InputValidator
from hybrid_intent_classifier import HybridIntentClassifier
import time
import uuid
from datetime import datetime
import logging

# Configure logging for demo purposes
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize validators
validator = InputValidator()
hybrid_classifier = HybridIntentClassifier(use_ml=True, ml_threshold=0.6)


def is_gibberish(text):
    """
    Detect if input is gibberish/nonsense text.
    Returns True if text appears to be gibberish.
    """
    import re
    
    # Remove whitespace and convert to lowercase
    clean_text = text.strip().lower()
    
    # Check 1: Too many repeated characters (e.g., "aaaaaaa", "dnksdnksdds")
    if len(set(clean_text.replace(" ", ""))) < 5:  # Less than 5 unique characters
        return True
    
    # Check 2: No vowels at all (except intentional acronyms which are usually short)
    vowels = set('aeiou')
    text_letters = [c for c in clean_text if c.isalpha()]
    if len(text_letters) > 10:  # Only check if text is substantial
        vowel_count = sum(1 for c in text_letters if c in vowels)
        vowel_ratio = vowel_count / len(text_letters) if text_letters else 0
        if vowel_ratio < 0.15:  # Less than 15% vowels is suspicious
            return True
    
    # Check 3: Too many consonant clusters (e.g., "dnksd", "mdsd")
    consonant_clusters = re.findall(r'[bcdfghjklmnpqrstvwxyz]{4,}', clean_text)
    if len(consonant_clusters) > 2:
        return True
    
    # Check 4: Repeated patterns (e.g., "asdasdasd", "dnkdnkdnk")
    words = clean_text.split()
    for word in words:
        if len(word) > 6:
            # Check if word is just repeated patterns
            for pattern_len in [2, 3, 4]:
                pattern = word[:pattern_len]
                if word == pattern * (len(word) // pattern_len) + pattern[:len(word) % pattern_len]:
                    return True
    
    # Check 5: No recognizable words (at least some common words should be present)
    common_words = {
        'i', 'me', 'my', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
        'feel', 'feeling', 'felt', 'think', 'thought', 'want', 'need', 'cant', 'cannot', 'can',
        'not', 'no', 'yes', 'the', 'a', 'an', 'and', 'or', 'but', 'very', 'so', 'too', 'all',
        'sad', 'happy', 'tired', 'exhausted', 'hopeless', 'worthless', 'depressed', 'anxious',
        'stressed', 'worried', 'scared', 'afraid', 'angry', 'upset', 'hurt', 'pain', 'help'
    }
    words_set = set(clean_text.split())
    if len(words_set) > 3:  # Only check if more than 3 words
        common_word_count = len(words_set & common_words)
        if common_word_count == 0:  # No common words at all
            return True
    
    return False


def is_not_describing_feelings(text):
    """
    Detect if the text is not actually describing feelings or mental state.
    Returns True if text is casual conversation, questions, or non-descriptive.
    """
    import re
    
    clean_text = text.strip().lower()
    
    # Common phrases that indicate user is NOT describing their feelings
    non_descriptive_patterns = [
        r'\bwhat should i (tell|say)\b',
        r'\bi don\'?t know what to (tell|say|write)\b',
        r'\bwhat do you (want|need|expect)\b',
        r'\bwhat am i supposed to (tell|say|write)\b',
        r'\bi\'?m not sure what to (tell|say|write)\b',
        r'\bhelp me\b.*\bwhat to (tell|say|write)\b',
        r'\btest(ing)?\b',
        r'\bhello\b',
        r'\bhi\b',
        r'\bhey\b',
        r'\bjust checking\b',
        r'\btrying (this|it) out\b',
        r'\blet\'?s see\b',
        r'\bdemo\b',
    ]
    
    for pattern in non_descriptive_patterns:
        if re.search(pattern, clean_text):
            return True
    
    # Check if text is mostly questions
    question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which']
    words = clean_text.split()
    question_count = sum(1 for word in words if word.rstrip('?.,!') in question_words)
    if question_count >= len(words) * 0.3:  # More than 30% questions
        return True
    
    # Check if text lacks emotional/feeling words
    emotion_keywords = {
        'feel', 'feeling', 'felt', 'sad', 'happy', 'angry', 'anxious', 'anxiety', 'depressed', 'depression',
        'worried', 'worry', 'scared', 'afraid', 'tired', 'exhausted', 'hopeless', 'worthless',
        'lonely', 'isolated', 'stressed', 'stress', 'overwhelmed', 'upset', 'hurt', 'pain',
        'empty', 'numb', 'guilty', 'guilt', 'shame', 'helpless', 'frustrated', 'irritated',
        'nervous', 'panic', 'crying', 'cry', 'sleep', 'appetite', 'energy', 'motivation',
        'concentration', 'focus', 'thoughts', 'thinking', 'mind', 'struggling', 'struggle',
        'suffering', 'suffer', 'mood', 'emotional', 'emotions'
    }
    
    words_set = set(clean_text.split())
    emotion_word_count = len(words_set & emotion_keywords)
    
    # If text is longer than 5 words but has NO emotion/feeling words, it's suspicious
    if len(words) > 5 and emotion_word_count == 0:
        return True
    
    return False


# Page configuration
st.set_page_config(
    page_title="MannKiBaat - AI Mental Health Screener",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# Professional Dark Mode Medical UI
st.markdown(
    """
    <style>
    /* Dark background */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Professional header with elegant gradient */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0;
        padding: 1.5rem 2rem 0.75rem 2rem;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: -0.5px;
        border-radius: 0.75rem 0.75rem 0 0;
        margin-left: -1rem;
        margin-right: -1rem;
        margin-top: -1rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #e0f2fe;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 0.75rem 2rem 1.5rem 2rem;
        margin-left: -1rem;
        margin-right: -1rem;
        margin-top: 0;
        border-radius: 0 0 0.75rem 0.75rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    }
    
    /* Medical disclaimer - dark mode */
    .disclaimer {
        background-color: #422006;
        padding: 1.25rem;
        border-radius: 0.75rem;
        border-left: 4px solid #f59e0b;
        margin: 1.5rem 0;
        font-size: 0.95rem;
        color: #fef3c7;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Privacy note - dark mode */
    .privacy-note {
        background-color: #0c4a6e;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 2px solid #0284c7;
        margin: 1.5rem 0;
        font-size: 0.9rem;
        color: #e0f2fe;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Input examples - dark mode */
    .example-hints {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0 1.5rem 0;
        font-size: 0.9rem;
        color: #cbd5e1;
        line-height: 1.8;
        border: 1px solid #334155;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Text input - dark mode */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 2px solid #475569 !important;
        border-radius: 0.5rem;
        font-size: 1rem;
        padding: 0.75rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stTextArea label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    /* Professional buttons - glowing effect */
    .stButton button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        transform: translateY(-2px);
    }
    
    /* Results display - dark cards */
    .result-box {
        padding: 2rem;
        border-radius: 0.75rem;
        margin: 1.5rem 0;
        border: 2px solid #334155;
        background-color: #1e293b;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    .result-box h2 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    .result-box p {
        color: #cbd5e1 !important;
    }
    
    .minimal-risk { 
        background-color: #064e3b;
        border-left: 6px solid #10b981;
        border-top: 1px solid #10b981;
    }
    .minimal-risk h2 {
        color: #6ee7b7 !important;
    }
    
    .mild-risk { 
        background-color: #1e3a8a;
        border-left: 6px solid #3b82f6;
        border-top: 1px solid #3b82f6;
    }
    .mild-risk h2 {
        color: #93c5fd !important;
    }
    
    .moderate-risk { 
        background-color: #78350f;
        border-left: 6px solid #f59e0b;
        border-top: 1px solid #f59e0b;
    }
    .moderate-risk h2 {
        color: #fcd34d !important;
    }
    
    .severe-risk { 
        background-color: #7f1d1d;
        border-left: 6px solid #ef4444;
        border-top: 1px solid #ef4444;
    }
    .severe-risk h2 {
        color: #fca5a5 !important;
    }
    
    /* Helpline box - enhanced dark mode */
    .helpline-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1.5rem 0;
        border: 2px solid #3b82f6;
        color: #ffffff;
        box-shadow: 0 8px 24px rgba(30, 64, 175, 0.4);
    }
    
    .helpline-box h3, .helpline-box h4 {
        color: #ffffff !important;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .helpline-box ul {
        margin-bottom: 1rem;
    }
    
    .helpline-box li {
        color: #e0f2fe !important;
        line-height: 1.8;
        margin-bottom: 0.5rem;
    }
    
    .helpline-box strong {
        color: #ffffff;
        font-weight: 600;
    }
    
    .helpline-box a {
        color: #93c5fd;
        text-decoration: none;
        font-weight: 600;
    }
    
    .helpline-box a:hover {
        color: #bfdbfe;
        text-decoration: underline;
    }
    
    /* PHQ-8 score display - glowing */
    .phq8-score {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
        color: #60a5fa;
        text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
    }
    
    /* Dark mode typography */
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-weight: 600;
    }
    
    p {
        color: #cbd5e1 !important;
        line-height: 1.6;
    }
    
    /* Streamlit overrides for dark mode */
    .stMarkdown {
        color: #cbd5e1 !important;
    }
    
    hr {
        border-color: #334155 !important;
    }
    
    /* Streamlit alerts - dark mode */
    .stAlert {
        background-color: #1e3a8a !important;
        border: 2px solid #3b82f6 !important;
        color: #e0f2fe !important;
        border-radius: 0.5rem !important;
    }
    
    .stSuccess {
        background-color: #064e3b !important;
        border: 2px solid #10b981 !important;
        color: #d1fae5 !important;
    }
    
    .stWarning {
        background-color: #78350f !important;
        border: 2px solid #f59e0b !important;
        color: #fef3c7 !important;
    }
    
    .stError {
        background-color: #7f1d1d !important;
        border: 2px solid #ef4444 !important;
        color: #fecaca !important;
    }
    
    .stInfo {
        background-color: #1e3a8a !important;
        border: 2px solid #3b82f6 !important;
        color: #dbeafe !important;
    }
    
    /* Expander - dark mode */
    .streamlit-expanderHeader {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #334155 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0f172a !important;
        border: 1px solid #475569 !important;
        color: #cbd5e1 !important;
    }
    
    /* Footer - dark mode */
    .branding-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 2px solid #334155;
    }
    
    /* Checkbox and other inputs */
    .stCheckbox label {
        color: #cbd5e1 !important;
    }
    
    /* Confidence badge - dark mode */
    .confidence-badge {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Header
st.markdown('<div class="main-header">🧠 MannKiBaat</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Mental Health Conversation Intelligence | Pre-Screening Filter</div>',
    unsafe_allow_html=True,
)


# Privacy Notice
st.markdown(
    """
    <div class="privacy-note">
        <strong>🔒 Your Privacy Matters</strong><br>
        • No data is stored or transmitted to external servers<br>
        • All processing happens locally in your browser session<br>
        • You can clear your session anytime using the button below
    </div>
    """,
    unsafe_allow_html=True,
)


# Disclaimer
st.markdown(
    """
    <div class="disclaimer">
        <strong>⚠️ Important Notice</strong><br>
        This tool uses conversation intelligence to identify genuine mental health discussions 
        and provides preliminary screening indicators. It is NOT a substitute for professional 
        diagnosis or clinical assessment. The sentiment analysis component requires clinical 
        validation before medical use. If you're experiencing mental health concerns, please 
        consult a licensed mental health professional.
    </div>
    """,
    unsafe_allow_html=True,
)


# Initialize session state with session ID and timestamp
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
    st.session_state.session_start = datetime.now()
    logger.info(f"New session started: {st.session_state.session_id}")


# Clean, professional section header
st.markdown("### Describe Your Recent Feelings")

# Example hints as text (not buttons) - professional and helpful
st.markdown(
    """
    <div class="example-hints">
        <strong>💡 Try describing:</strong><br>
        • "I've been feeling tired and sad for several weeks"<br>
        • "My sleep and appetite have changed recently"<br>
        • "I'm struggling with anxiety and can't concentrate"<br>
        • "Feeling hopeless and losing interest in activities"
    </div>
    """,
    unsafe_allow_html=True,
)


# Text input with session state
user_input = st.text_area(
    "How have you been feeling?",
    value=st.session_state.user_input,
    height=150,
    placeholder="Please describe your feelings and experiences in detail...",
    help="Your input is analyzed using the PHQ-8 validated depression screening tool",
    key="text_input",
)


# Professional buttons row
col1, col2 = st.columns([3, 1])

with col1:
    analyze_button = st.button(
        "🔍 Analyze Mental Health", type="primary", use_container_width=True
    )

with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        logger.info(f"Session {st.session_state.session_id}: Clearing session data")
        # Clear analysis data
        st.session_state.analysis_done = False
        st.session_state.user_input = ""
        if "result" in st.session_state:
            del st.session_state.result
        if "analysis_count" in st.session_state:
            del st.session_state.analysis_count
        # Keep session ID but log the clear
        logger.info("Session data cleared - privacy maintained")
        st.rerun()


# Analysis section with robust error handling
use_mock = False  # Always use production model
if analyze_button:
    # Comprehensive input validation using Hybrid Two-Stage Classifier
    if not user_input or len(user_input.strip()) < 10:
        st.error("⚠️ Please provide at least 10 characters describing your feelings.")
        logger.warning(
            f"Session {st.session_state.session_id}: Invalid input - too short"
        )
    elif is_gibberish(user_input):
        st.error("⚠️ Please provide meaningful text describing your feelings. The input appears to be random characters.")
        st.info("💡 **Tip:** Share genuine thoughts like 'I feel tired and unmotivated' or 'I'm feeling anxious about work'")
        logger.warning(
            f"Session {st.session_state.session_id}: Invalid input - detected gibberish"
        )
    else:
        # Use two-stage hybrid classifier (Rules + ML)
        classification = hybrid_classifier.classify_intent(user_input)
        
        is_valid = classification['is_valid']
        final_decision = classification['final_decision']
        confidence = classification['confidence']
        method = classification['method']
        
        logger.info(
            f"Session {st.session_state.session_id}: Classification={final_decision}, "
            f"Valid={is_valid}, Confidence={confidence:.1%}, Method={method}"
        )
        
        if not is_valid:
            # Show rejection message with examples
            st.warning(classification['message'])
            st.info(classification['examples'])
            
            # Show classification details in expander
            with st.expander("📊 Input Analysis"):
                st.write(f"**Decision:** {final_decision}")
                st.write(f"**Confidence:** {confidence:.1%}")
                st.write(f"**Method:** {method}")
                
                # Show both stages if hybrid
                if classification['stage1_result']:
                    st.write(f"**Stage 1 (Rules):** {classification['stage1_result']['type']}")
                if classification['stage2_result']:
                    ml_res = classification['stage2_result']
                    st.write(f"**Stage 2 (ML):** {ml_res['intent']} ({ml_res['confidence']:.1%})")
            
            logger.warning(
                f"Session {st.session_state.session_id}: Input rejected - {final_decision}"
            )
        else:
            # Log analysis start
            logger.info(f"Session {st.session_state.session_id}: Starting analysis")
            logger.info(f"Input length: {len(user_input)} characters")
            logger.info(f"Using mock model: {use_mock}")

            # Show loading spinner
            with st.spinner("🔄 Analyzing your input with PHQ-8 validated AI model..."):
                time.sleep(1)  # Brief pause for UX

                try:
                    # Perform analysis
                    logger.info("Calling PHQ-8 model...")
                    result = analyze_depression_risk(user_input, use_mock=use_mock)

                    # Log results
                    logger.info(
                        f"Analysis complete - Risk: {result['risk_level']}, "
                        f"Confidence: {result['confidence_percent']}, "
                        f"PHQ-8: {result['phq8_score']}"
                    )

                    st.session_state.analysis_done = True
                    st.session_state.result = result
                    st.session_state.result["timestamp"] = datetime.now()
                    st.session_state.analysis_count = (
                        st.session_state.get("analysis_count", 0) + 1
                    )

                    st.success("✅ Analysis completed successfully!")

                except ImportError as e:
                    logger.error(f"Import error: {str(e)}")
                    st.error("❌ Model dependencies not found. Attempting fallback...")
                    try:
                        # Fallback to mock model
                        logger.info("Falling back to mock model...")
                        result = analyze_depression_risk(user_input, use_mock=True)
                        st.session_state.analysis_done = True
                        st.session_state.result = result
                        st.session_state.result["timestamp"] = datetime.now()
                        st.warning(
                            "⚠️ Using demo model (mock). For production, ensure all dependencies are installed."
                        )
                    except Exception as fallback_error:
                        logger.error(f"Fallback failed: {str(fallback_error)}")
                        st.error(
                            f"❌ Both model and fallback failed: {str(fallback_error)}"
                        )

                except FileNotFoundError as e:
                    logger.error(f"Model file not found: {str(e)}")
                    st.error("❌ Model weights not found. Switching to demo mode...")
                    try:
                        result = analyze_depression_risk(user_input, use_mock=True)
                        st.session_state.analysis_done = True
                        st.session_state.result = result
                        st.session_state.result["timestamp"] = datetime.now()
                        st.info(
                            "ℹ️ Using demo model. Train the model using: python train_model.py"
                        )
                    except Exception as fallback_error:
                        logger.error(f"Fallback failed: {str(fallback_error)}")
                        st.error(f"❌ Analysis failed: {str(fallback_error)}")

                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
                    st.info("💡 Troubleshooting tips:")
                    st.info(
                        "1. Check that all dependencies are installed: pip install -r requirements.txt"
                    )
                    st.info("2. Try enabling Demo mode checkbox")
                    st.info("3. Ensure model weights are in model/fine_tuned_model/")

                    # Attempt one last fallback
                    try:
                        logger.info("Final fallback attempt...")
                        result = analyze_depression_risk(user_input, use_mock=True)
                        st.session_state.analysis_done = True
                        st.session_state.result = result
                        st.session_state.result["timestamp"] = datetime.now()
                        st.warning("⚠️ Recovered using demo model")
                    except:
                        pass


# Display results if analysis is done
if st.session_state.analysis_done and "result" in st.session_state:
    result = st.session_state.result

    st.markdown("---")
    st.markdown("## 📊 Assessment Results")

    # Determine risk class for styling
    risk_level = result["risk_level"]
    if risk_level == "Minimal":
        risk_class = "minimal-risk"
        emoji = "😊"
    elif risk_level == "Mild":
        risk_class = "mild-risk"
        emoji = "😐"
    elif risk_level == "Moderate":
        risk_class = "moderate-risk"
        emoji = "😟"
    elif risk_level == "Moderately Severe":
        risk_class = "severe-risk"
        emoji = "😰"
    else:  # Severe
        risk_class = "severe-risk"
        emoji = "🆘"

    # Results box
    st.markdown(
        f"""
        <div class="result-box {risk_class}">
            <h2 style="margin-top:0;">{emoji} Depression Severity: {risk_level}</h2>
            <div class="phq8-score">{result['phq8_score']}/27</div>
            <p style="text-align:center; font-size:1.1rem; margin:0;">
                <span class="confidence-badge" style="background:#003366; color:white;">
                    Confidence: {result['confidence_percent']}
                </span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Interpretation
    st.markdown(f"**Clinical Interpretation:**")
    st.info(result["interpretation"])

    # Enhanced: Display detected symptoms
    if "detected_symptoms" in result and len(result["detected_symptoms"]) > 0:
        st.markdown("### 📋 Detected PHQ-8 Symptoms")
        
        with st.expander(f"View Symptom Breakdown ({result['symptom_count']} symptoms detected)"):
            for detail in result["symptom_details"]:
                st.markdown(f"• {detail}")
            
            st.markdown("---")
            st.caption("*Symptom scoring based on frequency: 0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day*")
    
    # Enhanced: Display next steps
    if "next_steps" in result and len(result["next_steps"]) > 0:
        st.markdown("### 🎯 Recommended Next Steps")
        for step in result["next_steps"]:
            st.markdown(f"• {step}")

    # PHQ-8 Scale Reference
    with st.expander("📖 Understanding PHQ-8 Scores"):
        st.markdown(
            """
        **PHQ-8 Depression Severity Scale:**
        - **0-4:** Minimal depression
        - **5-9:** Mild depression
        - **10-14:** Moderate depression
        - **15-19:** Moderately severe depression
        - **20-27:** Severe depression
        
        *Your score helps mental health professionals assess depression severity and plan treatment.*
        
        **PHQ-8 Measures 8 Symptoms:**
        1. Anhedonia (loss of interest/pleasure)
        2. Depressed mood
        3. Sleep problems
        4. Fatigue/low energy
        5. Appetite changes
        6. Feelings of worthlessness/guilt
        7. Concentration problems
        8. Psychomotor changes (restlessness or slowing)
        
        Each symptom is scored 0-3 based on frequency over the past 2 weeks.
        """
        )

    # Indian Mental Health Resources
    st.markdown("---")
    st.markdown("## 📞 Mental Health Support Resources (India)")

    # Customize helpline based on severity
    if risk_level in ["Severe", "Moderately Severe"]:
        st.markdown(
            """
            <div class="helpline-box" style="border-color:#dc3545;">
                <h3 style="color:#dc3545; margin-top:0;">🆘 Immediate Help Available</h3>
                <p><strong>If you're in crisis or considering self-harm, please reach out NOW:</strong></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Helpline information
    st.markdown(
        """
        <div class="helpline-box">
            <h4 style="color: #ffffff; margin-top: 0;">🇮🇳 National Helplines</h4>
            <ul style="margin-bottom:1rem; list-style: none; padding-left: 0;">
                <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);"><strong>Vandrevala Foundation:</strong> <a href="tel:18602662345">1860-266-2345</a> | 24/7 Multilingual Support</li>
                <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);"><strong>iCall (TISS):</strong> <a href="tel:02225521111">022-2552-1111</a> | Mon-Sat, 8 AM - 10 PM</li>
                <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);"><strong>AASRA:</strong> <a href="tel:912227546669">91-22-2754-6669</a> | 24/7 Support</li>
                <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);"><strong>Snehi:</strong> <a href="tel:01165978181">011-6597-8181</a> | 24/7 Support</li>
                <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);"><strong>Mann Talks (NIMHANS):</strong> <a href="tel:08046110007">080-4611-0007</a> | Mon-Sat, 9 AM - 5 PM</li>
                <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);"><strong>Kiran Helpline:</strong> <a href="tel:18005990019">1800-599-0019</a> | 24/7</li>
                <li style="padding: 0.5rem 0;"><strong>NIMHANS Telemedicine:</strong> <a href="tel:08026995000">080-2699-5000</a></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Additional resources with cultural context
    st.markdown("### 🌟 Additional Support Options")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **Professional Help:**
        - Consult a psychiatrist or psychologist
        - Visit nearest community health center
        - Check NIMHANS telemedicine services
        - Employee Assistance Programs (if available)
        """
        )

    with col2:
        st.markdown(
            """
        **Self-Care Practices:**
        - Practice mindfulness & meditation
        - Regular physical activity
        - Maintain sleep hygiene
        - Connect with supportive friends/family
        """
        )

    # Model info
    if result.get("used_mock"):
        st.caption(
            "ℹ️ *Assessment performed using demo model. For production use, deploy with fine-tuned DistilBERT model.*"
        )
    else:
        st.caption(
            "✅ *Assessment performed using fine-tuned DistilBERT model with PHQ-8 validation.*"
        )


# Footer with branding
st.markdown(
    """
    <div class="branding-footer">
        <strong>MannKiBaat</strong> - Mental Health Screening Tool<br>
        Powered by DistilBERT | PHQ-8 Validated | Made with ❤️ for Mental Health Awareness<br>
        <em>Remember: Seeking help is a sign of strength, not weakness.</em>
    </div>
    """,
    unsafe_allow_html=True,
)
