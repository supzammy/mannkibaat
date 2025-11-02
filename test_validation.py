"""Test improved validation for casual/non-descriptive text"""
import re


def is_not_describing_feelings(text):
    """
    Detect if the text is not actually describing feelings or mental state.
    Returns True if text is casual conversation, questions, or non-descriptive.
    """
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
            return True, f"Matched pattern: {pattern}"
    
    # Check if text is mostly questions
    question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which']
    words = clean_text.split()
    question_count = sum(1 for word in words if word.rstrip('?.,!') in question_words)
    if question_count >= len(words) * 0.3:  # More than 30% questions
        return True, f"Too many questions: {question_count}/{len(words)}"
    
    # Check if text lacks emotional/feeling words
    emotion_keywords = {
        'feel', 'feeling', 'felt', 'sad', 'happy', 'angry', 'anxious', 'depressed',
        'worried', 'scared', 'afraid', 'tired', 'exhausted', 'hopeless', 'worthless',
        'lonely', 'isolated', 'stressed', 'overwhelmed', 'upset', 'hurt', 'pain',
        'empty', 'numb', 'guilty', 'shame', 'helpless', 'frustrated', 'irritated',
        'nervous', 'panic', 'crying', 'sleep', 'appetite', 'energy', 'motivation',
        'concentration', 'focus', 'thoughts', 'thinking', 'mind'
    }
    
    words_set = set(clean_text.split())
    emotion_word_count = len(words_set & emotion_keywords)
    
    # If text is longer than 5 words but has NO emotion/feeling words, it's suspicious
    if len(words) > 5 and emotion_word_count == 0:
        return True, f"No emotional words found (text has {len(words)} words)"
    
    return False, "Valid - describes feelings"


# Test cases
test_cases = [
    # Should be rejected (not describing feelings)
    "bro what should i tell you",
    "what do you want me to say",
    "i don't know what to write here",
    "just testing this out",
    "hello how are you",
    "what am i supposed to tell",
    
    # Should be accepted (describing feelings)
    "I feel tired and unmotivated lately",
    "I'm struggling with anxiety and depression",
    "I feel sad and hopeless most days",
    "Can't sleep, feel exhausted all the time",
    "I'm worried about everything and can't focus",
    "Feeling overwhelmed and stressed at work",
]

print("=" * 70)
print("VALIDATION TEST: Is NOT Describing Feelings")
print("=" * 70)

for test in test_cases:
    is_invalid, reason = is_not_describing_feelings(test)
    status = "❌ REJECT" if is_invalid else "✅ ACCEPT"
    print(f'\n{status}: "{test}"')
    print(f"   Reason: {reason}")

print("\n" + "=" * 70)
