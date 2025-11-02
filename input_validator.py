"""
Input Validation Module for MannKiBaat
Filters out casual/conversational inputs and validates genuine mental health content.
"""

import re
from typing import Tuple, Dict, List


class InputValidator:
    """Validates user input to ensure genuine mental health descriptions."""

    # Prompt 1: Casual Text Detection
    # These are phrases that indicate casual conversation, not genuine mental health descriptions
    CASUAL_PHRASES = [
        # English casual terms
        "bro",
        "lol",
        "lmao",
        "rofl",
        "idk",
        "dunno",
        "what should i tell you",
        "what should i say",
        "what do you want",
        # Removed "nothing" - too general, catches genuine phrases like "nothing makes me happy"
        "idk what to say",
        "don't know what to say",
        "what am i supposed to say",
        "what am i supposed to tell",
        "just testing",
        "testing this",
        # Removed standalone "test" - too aggressive, catches "test anxiety"
        "hello",
        "hi",
        "hey",
        "sup",
        "whats up",
        "how are you",
        "demo",
        # Indian casual terms
        "yaar",
        "yar",
        "bhai",
        "kya bolu",
        "kya bolun",
        "kuch nahi",
        "pata nahi",
        "samajh nahi aa raha",
        "kaise batau",
    ]

    # Prompt 2: Feeling Word Dictionary
    POSITIVE_FEELINGS = {
        "good",
        "happy",
        "fine",
        "okay",
        "ok",
        "great",
        "better",
        "improving",
        "positive",
        "motivated",
        "energized",
        "hopeful",
        "content",
        "peaceful",
        "calm",
        "relaxed",
        "cheerful",
        "joyful",
        # Indian English variations
        "theek",
        "acha",
        "badiya",
    }

    NEGATIVE_FEELINGS = {
        "sad",
        "depressed",
        "depression",
        "anxious",
        "anxiety",
        "worried",
        "worry",
        "worried",
        "worrying",
        "tired",
        "exhausted",
        "hopeless",
        "worthless",
        "empty",
        "lonely",
        "isolated",
        "stressed",
        "stress",
        "stressful",
        "overwhelmed",
        "upset",
        "hurt",
        "pain",
        "suffering",
        "miserable",
        "unhappy",
        "down",
        "low",
        "blue",
        "guilty",
        "guilt",
        "shame",
        "helpless",
        "frustrated",
        "irritated",
        "angry",
        "rage",
        "nervous",
        "panic",
        "scared",
        "afraid",
        "fearful",
        "crying",
        "cry",
        "tears",
        "numb",
        "lifeless",
        "suicidal",
        "dying",
        "hopeless",
        # Indian English variations
        "dukhi",
        "udaas",
        "pareshan",
        "tension",
    }
    
    PHYSICAL_SYMPTOMS = {
        "sleep",
        "sleeping",
        "insomnia",
        "sleepless",
        "awake",
        "nightmare",
        "appetite",
        "eating",
        "hunger",
        "food",
        "weight",
        "energy",
        "fatigue",
        "focus",
        "concentration",
        "attention",
        "memory",
        "headache",
        "pain",
        "ache",
        "stomach",
        "nausea",
        "dizzy",
        "weak",
        "trembling",
        "shaking",
        "racing heart",
        "breathless",
        "chest pain",
    }
    
    MENTAL_DESCRIPTORS = {
        "feel",
        "feeling",
        "felt",
        "think",
        "thinking",
        "thought",
        "thoughts",
        "mind",
        "mental",
        "emotional",
        "emotions",
        "mood",
        "state",
        "struggling",
        "struggle",
        "suffering",
        "suffer",
        "experiencing",
        "going through",
        "dealing with",
        "coping",
        "managing",
        "handling",
        "everything",  # Common in "worried about everything"
        "anything",    # Common in "can't do anything"
        "nothing",     # Common in "feel nothing" (but check context)
    }    # Combined feeling keywords
    ALL_FEELING_KEYWORDS = (
        POSITIVE_FEELINGS
        | NEGATIVE_FEELINGS
        | PHYSICAL_SYMPTOMS
        | MENTAL_DESCRIPTORS
    )

    # Question patterns that don't describe feelings
    QUESTION_PATTERNS = [
        r"\bwhat should i (tell|say|write)\b",
        r"\bi don\'?t know what to (tell|say|write)\b",
        r"\bwhat do you (want|need|expect)\b",
        r"\bwhat am i supposed to (tell|say|write)\b",
        r"\bhow (does|do) (this|it) work\b",
        r"\bcan you help me\b",
        r"\bwhat is this\b",
    ]

    def __init__(self):
        """Initialize the validator."""
        pass

    def validate_input(self, text: str) -> Tuple[bool, str, Dict]:
        """
        Main validation pipeline (Prompt 3).

        Args:
            text: User input text

        Returns:
            Tuple of (is_valid, validation_type, metadata)
            - is_valid: True if input should be analyzed, False otherwise
            - validation_type: "genuine", "casual", "short", "question", "neutral"
            - metadata: Additional information about the validation
        """
        if not text or not text.strip():
            return False, "empty", {"message": "Input is empty"}

        text_lower = text.lower().strip()
        words = text.split()
        word_count = len(words)

        # Step 1: Check for casual/conversational input
        # Use word boundaries to avoid false matches (e.g., "hi" in "think")
        for phrase in self.CASUAL_PHRASES:
            # For multi-word phrases, use substring match
            if " " in phrase:
                if phrase in text_lower:
                    return False, "casual", {
                        "message": "Casual conversation detected",
                        "matched_phrase": phrase,
                    }
            else:
                # For single words, use word boundary matching
                pattern = r'\b' + re.escape(phrase) + r'\b'
                if re.search(pattern, text_lower):
                    return False, "casual", {
                        "message": "Casual conversation detected",
                        "matched_phrase": phrase,
                    }

        # Step 2: Check for question patterns
        for pattern in self.QUESTION_PATTERNS:
            if re.search(pattern, text_lower):
                return False, "question", {
                    "message": "Non-descriptive question detected",
                    "matched_pattern": pattern,
                }

        # Step 3: Check word count
        if word_count < 5:
            return False, "short", {
                "message": "Input too short (less than 5 words)",
                "word_count": word_count,
            }

        # Step 4: Check for feeling-related keywords
        words_set = set(text_lower.split())
        feeling_matches = words_set & self.ALL_FEELING_KEYWORDS

        if feeling_matches:
            return True, "genuine", {
                "message": "Genuine feeling description detected",
                "matched_keywords": list(feeling_matches),
                "keyword_count": len(feeling_matches),
            }

        # Step 5: Check for too many non-feeling words (neutral/descriptive but not emotional)
        if word_count > 5 and not feeling_matches:
            return False, "neutral", {
                "message": "No emotional/feeling keywords found",
                "word_count": word_count,
            }

        # Default: allow if not caught by other filters
        return True, "accepted", {"message": "Input accepted"}

    def is_gibberish(self, text: str) -> bool:
        """
        Check if text is gibberish (random characters).

        Args:
            text: Input text

        Returns:
            True if gibberish, False otherwise
        """
        clean_text = text.strip().lower()

        # Too few unique characters
        if len(set(clean_text.replace(" ", ""))) < 5:
            return True

        # Check vowel ratio
        vowels = set("aeiou")
        text_letters = [c for c in clean_text if c.isalpha()]
        if len(text_letters) > 10:
            vowel_count = sum(1 for c in text_letters if c in vowels)
            vowel_ratio = vowel_count / len(text_letters) if text_letters else 0
            if vowel_ratio < 0.15:
                return True

        # Too many consonant clusters
        consonant_clusters = re.findall(r"[bcdfghjklmnpqrstvwxyz]{4,}", clean_text)
        if len(consonant_clusters) > 2:
            return True

        return False

    def get_smart_response(self, validation_type: str) -> Dict[str, str]:
        """
        Get intelligent response based on validation type (Prompt 4).

        Args:
            validation_type: Type from validate_input

        Returns:
            Dict with 'message' and 'examples'
        """
        responses = {
            "casual": {
                "message": "⚠️ Please share how you've actually been feeling emotionally and physically.",
                "examples": (
                    "💡 **Try describing:**\n"
                    "- 'I've been feeling tired and sad lately'\n"
                    "- 'I'm struggling with anxiety and can't sleep'\n"
                    "- 'My mood has been low and I have no energy'"
                ),
            },
            "question": {
                "message": "⚠️ This tool analyzes your emotional state. Please describe how you've been feeling.",
                "examples": (
                    "💡 **Examples:**\n"
                    "- 'I feel anxious and overwhelmed most days'\n"
                    "- 'I'm experiencing sadness and lack of motivation'\n"
                    "- 'I've been having trouble sleeping and concentrating'"
                ),
            },
            "short": {
                "message": "⚠️ Could you describe more about your mood, sleep, and energy levels?",
                "examples": (
                    "💡 **Please share more details about:**\n"
                    "- How you've been feeling emotionally\n"
                    "- Changes in sleep, appetite, or energy\n"
                    "- Physical symptoms you're experiencing\n"
                    "- Duration of these feelings"
                ),
            },
            "neutral": {
                "message": "⚠️ Please describe your emotional and mental state more specifically.",
                "examples": (
                    "💡 **Include information about:**\n"
                    "- Your current mood (sad, anxious, worried, etc.)\n"
                    "- Physical symptoms (fatigue, sleep issues, appetite changes)\n"
                    "- How long you've been feeling this way\n"
                    "- Impact on daily activities"
                ),
            },
            "empty": {
                "message": "⚠️ Please provide a description of how you've been feeling.",
                "examples": (
                    "💡 **Share your thoughts like:**\n"
                    "- 'I feel constantly tired and unmotivated'\n"
                    "- 'I'm worried and stressed about everything'\n"
                    "- 'I feel sad and empty most of the time'"
                ),
            },
        }

        return responses.get(
            validation_type,
            {
                "message": "Please describe your feelings in more detail.",
                "examples": "Include information about your mood, energy, and any changes you've noticed.",
            },
        )

    def extract_feeling_content(self, text: str) -> Tuple[str, int]:
        """
        Extract feeling-related content from mixed input.

        Args:
            text: Input text

        Returns:
            Tuple of (extracted_text, match_count)
        """
        sentences = re.split(r"[.!?]+", text)
        feeling_sentences = []

        for sentence in sentences:
            sentence_lower = sentence.lower()
            words_set = set(sentence_lower.split())
            matches = words_set & self.ALL_FEELING_KEYWORDS

            if matches:
                feeling_sentences.append(sentence.strip())

        extracted = ". ".join(feeling_sentences)
        match_count = len(feeling_sentences)

        return extracted, match_count

    def get_validation_stats(self, text: str) -> Dict:
        """
        Get detailed statistics about the input.

        Args:
            text: Input text

        Returns:
            Dict with validation statistics
        """
        text_lower = text.lower()
        words = text.split()
        words_set = set(text_lower.split())

        return {
            "word_count": len(words),
            "char_count": len(text),
            "positive_feelings": len(words_set & self.POSITIVE_FEELINGS),
            "negative_feelings": len(words_set & self.NEGATIVE_FEELINGS),
            "physical_symptoms": len(words_set & self.PHYSICAL_SYMPTOMS),
            "mental_descriptors": len(words_set & self.MENTAL_DESCRIPTORS),
            "total_feeling_keywords": len(words_set & self.ALL_FEELING_KEYWORDS),
            "is_gibberish": self.is_gibberish(text),
        }


# Convenience function for quick validation
def validate_user_input(text: str) -> Tuple[bool, str, Dict]:
    """
    Quick validation function.

    Args:
        text: User input

    Returns:
        Tuple of (is_valid, validation_type, metadata)
    """
    validator = InputValidator()
    return validator.validate_input(text)
