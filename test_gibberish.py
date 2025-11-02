"""Test gibberish detection"""
import re


def is_gibberish(text):
    """
    Detect if input is gibberish/nonsense text.
    Returns True if text appears to be gibberish.
    """
    # Remove whitespace and convert to lowercase
    clean_text = text.strip().lower()
    
    # Check 1: Too many repeated characters (e.g., "aaaaaaa", "dnksdnksdds")
    if len(set(clean_text.replace(" ", ""))) < 5:  # Less than 5 unique characters
        return True, "Too few unique characters"
    
    # Check 2: No vowels at all (except intentional acronyms which are usually short)
    vowels = set('aeiou')
    text_letters = [c for c in clean_text if c.isalpha()]
    if len(text_letters) > 10:  # Only check if text is substantial
        vowel_count = sum(1 for c in text_letters if c in vowels)
        vowel_ratio = vowel_count / len(text_letters) if text_letters else 0
        if vowel_ratio < 0.15:  # Less than 15% vowels is suspicious
            return True, f"Low vowel ratio: {vowel_ratio:.2%}"
    
    # Check 3: Too many consonant clusters (e.g., "dnksd", "mdsd")
    consonant_clusters = re.findall(r'[bcdfghjklmnpqrstvwxyz]{4,}', clean_text)
    if len(consonant_clusters) > 2:
        return True, f"Too many consonant clusters: {consonant_clusters}"
    
    # Check 4: Repeated patterns (e.g., "asdasdasd", "dnkdnkdnk")
    words = clean_text.split()
    for word in words:
        if len(word) > 6:
            # Check if word is just repeated patterns
            for pattern_len in [2, 3, 4]:
                pattern = word[:pattern_len]
                if word == pattern * (len(word) // pattern_len) + pattern[:len(word) % pattern_len]:
                    return True, f"Repeated pattern in word: {word}"
    
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
            return True, "No common words found"
    
    return False, "Valid text"


# Test cases
test_cases = [
    "dnksdnksdds md",  # Your example
    "asdasdasdasd",  # Repeated pattern
    "aaaaaaaaaa bbbbb",  # Repeated characters
    "I feel sad and tired",  # Valid
    "Feeling anxious about work",  # Valid
    "xyzpqrst mnbvcxz",  # No vowels
    "I'm feeling really exhausted and hopeless",  # Valid
    "qwerty uiop asdf",  # Keyboard mashing
]

print("=" * 70)
print("GIBBERISH DETECTION TEST RESULTS")
print("=" * 70)

for test in test_cases:
    is_bad, reason = is_gibberish(test)
    status = "❌ GIBBERISH" if is_bad else "✅ VALID"
    print(f'\n{status}: "{test}"')
    print(f"   Reason: {reason}")

print("\n" + "=" * 70)
