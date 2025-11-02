"""
Enhanced PHQ-8 Symptom Detection with 300+ Clinical Terms
Maps user text to PHQ-8 scoring system (0-3 per symptom, 0-27 total)

PHQ-8 Symptom Domains:
1. Anhedonia (Loss of interest/pleasure)
2. Depressed Mood
3. Sleep Problems
4. Fatigue/Energy Loss
5. Appetite Changes
6. Feelings of Worthlessness/Guilt
7. Concentration Problems
8. Psychomotor Changes
"""

import re
from typing import Dict, List, Tuple


class PHQ8SymptomDetector:
    """Enhanced symptom detection with frequency mapping"""
    
    def __init__(self):
        # PHQ-8 Symptom 1: Anhedonia - Loss of interest or pleasure
        self.anhedonia_keywords = {
            # Core clinical terms
            'anhedonia', 'no pleasure', 'no joy', 'no interest', 'no motivation',
            'lost interest', 'lost pleasure', 'nothing feels good', 'nothing enjoyable',
            'dont enjoy', "don't enjoy", 'cant enjoy', "can't enjoy", 'no enjoyment',
            
            # Activity-specific
            'nothing interests me', 'nothing excites me', 'everything boring',
            'no fun anymore', 'stopped caring', 'dont care anymore', "don't care anymore",
            'nothing matters', 'lost passion', 'no desire', 'no excitement',
            
            # Emotional flatness
            'feel nothing', 'feel empty', 'emotionally numb', 'numb inside',
            'cant feel anything', "can't feel anything", 'no feelings', 'emotionally dead',
            'feel flat', 'feel blank', 'hollow inside', 'empty inside',
            
            # Social withdrawal related
            'dont want to do anything', "don't want to do anything", 
            'stopped doing things i love', 'gave up hobbies', 'no motivation for',
            'dont want to see people', "don't want to see people", 'withdrawn',
            'isolating myself', 'no interest in socializing',
            
            # Severity indicators
            'nothing brings joy', 'nothing makes me happy', 'pleasure in nothing',
            'interest in nothing', 'apathetic', 'indifferent to everything',
        }
        
        # PHQ-8 Symptom 2: Depressed Mood
        self.depressed_mood_keywords = {
            # Core depression terms
            'depressed', 'depression', 'feeling down', 'feeling low', 'down in dumps',
            'feeling blue', 'melancholy', 'despondent', 'dejected', 'gloomy',
            
            # Hopelessness
            'hopeless', 'no hope', 'hopelessness', 'feeling hopeless', 'lost hope',
            'no future', 'no way out', 'never get better', 'pointless', 'meaningless',
            'whats the point', "what's the point", 'why bother', 'no point',
            
            # Sadness variations
            'sad', 'sadness', 'miserable', 'unhappy', 'crying', 'tearful', 'weeping',
            'cry all the time', 'cant stop crying', "can't stop crying", 'sobbing',
            'tears', 'broken inside', 'heartbroken', 'devastated',
            
            # Despair
            'despair', 'desperate', 'anguish', 'suffering', 'tormented', 'tortured',
            'agony', 'pain inside', 'emotional pain', 'hurting inside', 'darkness',
            'dark place', 'drowning', 'sinking', 'falling apart', 'breaking down',
            
            # Mood descriptors
            'mood is bad', 'terrible mood', 'awful mood', 'mood swings',
            'feel terrible', 'feel awful', 'feel horrible', 'feel miserable',
            'cant be happy', "can't be happy", 'never happy anymore',
        }
        
        # PHQ-8 Symptom 3: Sleep Problems
        self.sleep_keywords = {
            # Insomnia
            'insomnia', 'cant sleep', "can't sleep", 'cannot sleep', 'trouble sleeping',
            'difficulty sleeping', 'hard to fall asleep', 'cant fall asleep',
            'lying awake', 'tossing and turning', 'awake all night', 'no sleep',
            'sleepless', 'sleep deprived', 'sleep deprivation',
            
            # Early waking
            'wake up early', 'waking up early', 'wake at 3am', 'wake at 4am',
            'cant stay asleep', "can't stay asleep", 'wake up middle of night',
            'early morning waking', 'early awakening',
            
            # Hypersomnia
            'sleeping too much', 'sleep all day', 'oversleeping', 'cant get out of bed',
            "can't get out of bed", 'hypersomnia', 'sleep 12 hours', 'sleep 14 hours',
            'always sleeping', 'sleep excessively', 'excessive sleep',
            
            # Sleep quality
            'poor sleep', 'bad sleep', 'restless sleep', 'disturbed sleep',
            'nightmares', 'bad dreams', 'sleep problems', 'sleep issues',
            'never feel rested', 'tired after sleeping', 'unrefreshing sleep',
            
            # Sleep patterns
            'irregular sleep', 'sleep schedule messed up', 'sleep pattern disrupted',
            'sleep too little', 'sleep too much', 'sleep problems every night',
        }
        
        # PHQ-8 Symptom 4: Fatigue/Low Energy
        self.energy_keywords = {
            # Fatigue
            'tired', 'fatigue', 'fatigued', 'exhausted', 'exhaustion', 'drained',
            'worn out', 'burnt out', 'burned out', 'burnout', 'wiped out',
            'completely drained', 'no energy', 'low energy', 'lack of energy',
            
            # Physical sensations
            'heavy', 'body feels heavy', 'limbs feel heavy', 'weighed down',
            'sluggish', 'lethargic', 'lethargy', 'weak', 'weakness', 'feeble',
            'no strength', 'lack of stamina', 'cant move', "can't move",
            
            # Activity impact
            'too tired to', 'no energy for', 'cant do anything', "can't do anything",
            'everything exhausting', 'simple tasks exhausting', 'basic tasks difficult',
            'need to rest constantly', 'always tired', 'tired all the time',
            'chronically tired', 'perpetually exhausted',
            
            # Morning/daily patterns
            'cant get up', "can't get up", 'cant wake up', "can't wake up",
            'morning exhaustion', 'tired in morning', 'no energy in morning',
            'tired all day', 'energy crashes', 'low energy all day',
            
            # Severity
            'completely exhausted', 'utterly drained', 'bone tired', 'dead tired',
            'too tired to function', 'cant function', "can't function", 'debilitating fatigue',
        }
        
        # PHQ-8 Symptom 5: Appetite/Weight Changes
        self.appetite_keywords = {
            # Decreased appetite
            'no appetite', 'lost appetite', 'poor appetite', 'lack of appetite',
            'dont want to eat', "don't want to eat", 'cant eat', "can't eat",
            'food doesnt taste good', "food doesn't taste good", 'no interest in food',
            'forcing myself to eat', 'forgetting to eat', 'skipping meals',
            
            # Increased appetite
            'eating too much', 'overeating', 'cant stop eating', "can't stop eating",
            'eating constantly', 'always hungry', 'increased appetite', 'binge eating',
            'emotional eating', 'comfort eating', 'stress eating',
            
            # Weight changes
            'lost weight', 'weight loss', 'losing weight', 'dropped weight',
            'gained weight', 'weight gain', 'gaining weight', 'put on weight',
            'unintentional weight loss', 'unintentional weight gain',
            
            # Eating patterns
            'irregular eating', 'eating disorder', 'not eating enough',
            'eating habits changed', 'appetite changed', 'taste changed',
            'everything tasteless', 'food tastes like nothing',
        }
        
        # PHQ-8 Symptom 6: Feelings of Worthlessness/Guilt
        self.worthlessness_keywords = {
            # Core worthlessness
            'worthless', 'worthlessness', 'feel worthless', 'no worth', 'no value',
            'useless', 'feel useless', 'good for nothing', 'waste of space',
            'burden', 'burden to others', 'burden on family', 'everyone better without me',
            
            # Self-blame
            'all my fault', 'blame myself', 'self blame', 'its my fault', "it's my fault",
            'i ruined everything', 'i mess everything up', 'always my fault',
            'disappointing everyone', 'let everyone down', 'failed everyone',
            
            # Guilt
            'guilty', 'guilt', 'feeling guilty', 'guilty all the time',
            'guilty for existing', 'guilty about everything', 'constant guilt',
            'overwhelming guilt', 'cant forgive myself', "can't forgive myself",
            
            # Failure
            'failure', 'feel like a failure', 'complete failure', 'failed at life',
            'cant do anything right', "can't do anything right", 'nothing goes right',
            'always failing', 'loser', 'feel like a loser',
            
            # Self-deprecation
            'hate myself', 'self hatred', 'self loathing', 'disgusted with myself',
            'ashamed', 'shame', 'embarrassed to exist', 'pathetic',
            'inadequate', 'not good enough', 'never good enough', 'defective',
            'broken', 'damaged', 'flawed', 'inferior',
        }
        
        # PHQ-8 Symptom 7: Concentration/Thinking Problems
        self.concentration_keywords = {
            # Focus issues
            'cant concentrate', "can't concentrate", 'cant focus', "can't focus",
            'no focus', 'no concentration', 'poor concentration', 'difficulty concentrating',
            'trouble focusing', 'difficulty focusing', 'attention problems',
            'scattered', 'distracted', 'easily distracted',
            
            # Cognitive impairment
            'brain fog', 'foggy brain', 'mind is foggy', 'head feels foggy',
            'confused', 'confusion', 'cant think clearly', "can't think clearly",
            'thoughts muddled', 'mind racing', 'racing thoughts', 'intrusive thoughts',
            
            # Memory problems
            'forgetful', 'memory problems', 'cant remember', "can't remember",
            'forgetting everything', 'memory is bad', 'short term memory',
            'forget what i was doing', 'lose track', 'spacing out',
            
            # Decision making
            'cant make decisions', "can't make decisions", 'difficulty deciding',
            'indecisive', 'overwhelmed by decisions', 'paralyzed by choices',
            'overthinking', 'overthinking everything',
            
            # Work/study impact
            'cant work', "can't work", 'cant study', "can't study",
            'cant read', "can't read", 'cant follow conversations',
            'losing productivity', 'work suffering', 'grades dropping',
        }
        
        # PHQ-8 Symptom 8: Psychomotor Changes
        self.psychomotor_keywords = {
            # Slowed down
            'moving slowly', 'slow movements', 'sluggish', 'slowed down',
            'everything in slow motion', 'cant move normally', "can't move normally",
            'heavy limbs', 'movements feel heavy', 'psychomotor retardation',
            
            # Agitation
            'restless', 'restlessness', 'cant sit still', "can't sit still",
            'fidgety', 'fidgeting', 'pacing', 'cant relax', "can't relax",
            'agitated', 'agitation', 'jittery', 'nervous energy',
            'on edge', 'tense', 'tension', 'wound up',
            
            # Physical manifestations
            'trembling', 'shaking', 'hands shaking', 'body shaking',
            'motor coordination problems', 'clumsy', 'dropping things',
            'movements jerky', 'twitching',
        }
        
        # Frequency indicators (0-3 scale)
        self.frequency_patterns = {
            0: {  # Not at all
                'not', 'never', 'no longer', 'dont have', "don't have",
                'not experiencing', 'not feeling', 'none',
            },
            1: {  # Several days
                'sometimes', 'occasionally', 'few times', 'several days',
                'once in a while', 'here and there', 'now and then',
                'some days', 'few days a week',
            },
            2: {  # More than half the days
                'often', 'frequently', 'most days', 'more than half',
                'majority of days', 'usually', 'regularly', 'most of the time',
                '5 days a week', '4 days a week',
            },
            3: {  # Nearly every day
                'every day', 'everyday', 'daily', 'constantly', 'always',
                'all the time', 'continuously', 'non stop', 'non-stop',
                'never stops', '24/7', 'every single day', 'all day every day',
                'nearly every day', 'almost every day', 'every night',
            }
        }
        
        # Additional clinical indicators
        self.severity_amplifiers = {
            'severe', 'extreme', 'intense', 'overwhelming', 'unbearable',
            'crushing', 'debilitating', 'crippling', 'devastating', 'terrible',
            'horrible', 'awful', 'worst', 'cant take it', "can't take it",
            'cant handle', "can't handle", 'too much',
        }
        
        # Duration indicators
        self.duration_indicators = {
            'weeks': 2,  # multiplier for scoring
            'months': 3,
            'years': 4,
            'long time': 3,
            'forever': 4,
        }
    
    def detect_symptom_frequency(self, text: str, symptom_keywords: set) -> Tuple[bool, int]:
        """
        Detect if symptom is present and estimate frequency (0-3)
        
        Returns:
            (symptom_present: bool, frequency_score: int)
        """
        text_lower = text.lower()
        
        # Check if symptom keywords present
        symptom_present = any(keyword in text_lower for keyword in symptom_keywords)
        
        if not symptom_present:
            return False, 0
        
        # Detect frequency level
        frequency_score = 1  # Default: several days
        
        # Check for frequency patterns (highest match wins)
        for score in [3, 2, 1, 0]:
            if any(pattern in text_lower for pattern in self.frequency_patterns[score]):
                frequency_score = score
                break
        
        # Check for severity amplifiers (increase score)
        if any(amp in text_lower for amp in self.severity_amplifiers):
            frequency_score = min(3, frequency_score + 1)
        
        # Check for duration indicators (increase score)
        for duration, multiplier in self.duration_indicators.items():
            if duration in text_lower:
                frequency_score = min(3, int(frequency_score * 1.5))
                break
        
        return True, frequency_score
    
    def analyze_symptoms(self, text: str) -> Dict:
        """
        Analyze text for all PHQ-8 symptoms
        
        Returns:
            Dict with symptom scores and total PHQ-8 score
        """
        results = {
            'symptoms': {},
            'total_score': 0,
            'severity': '',
            'detected_symptoms': [],
            'symptom_details': []
        }
        
        # Analyze each symptom domain
        symptom_domains = {
            'Anhedonia': self.anhedonia_keywords,
            'Depressed Mood': self.depressed_mood_keywords,
            'Sleep Problems': self.sleep_keywords,
            'Fatigue/Low Energy': self.energy_keywords,
            'Appetite Changes': self.appetite_keywords,
            'Worthlessness/Guilt': self.worthlessness_keywords,
            'Concentration Problems': self.concentration_keywords,
            'Psychomotor Changes': self.psychomotor_keywords,
        }
        
        for symptom_name, keywords in symptom_domains.items():
            present, frequency = self.detect_symptom_frequency(text, keywords)
            
            results['symptoms'][symptom_name] = {
                'present': present,
                'frequency_score': frequency,
                'description': self._get_frequency_description(frequency)
            }
            
            results['total_score'] += frequency
            
            if present and frequency > 0:
                results['detected_symptoms'].append(symptom_name)
                results['symptom_details'].append(
                    f"{symptom_name}: {self._get_frequency_description(frequency)} (Score: {frequency}/3)"
                )
        
        # Determine severity
        results['severity'] = self._map_score_to_severity(results['total_score'])
        
        return results
    
    def _get_frequency_description(self, score: int) -> str:
        """Map frequency score to description"""
        descriptions = {
            0: "Not at all",
            1: "Several days",
            2: "More than half the days",
            3: "Nearly every day"
        }
        return descriptions.get(score, "Unknown")
    
    def _map_score_to_severity(self, total_score: int) -> str:
        """Map total PHQ-8 score to severity level"""
        if total_score <= 4:
            return "Minimal"
        elif total_score <= 9:
            return "Mild"
        elif total_score <= 14:
            return "Moderate"
        elif total_score <= 19:
            return "Moderately Severe"
        else:
            return "Severe"
    
    def get_clinical_interpretation(self, results: Dict) -> str:
        """Generate clinical interpretation text"""
        score = results['total_score']
        severity = results['severity']
        
        interpretations = {
            "Minimal": f"Your PHQ-8 score of {score} suggests minimal depression symptoms. Continue monitoring your mental health and maintain healthy habits.",
            "Mild": f"Your PHQ-8 score of {score} indicates mild depression. Consider talking to someone you trust, a counselor, or exploring self-help resources.",
            "Moderate": f"Your PHQ-8 score of {score} suggests moderate depression. Professional consultation with a therapist or counselor is recommended.",
            "Moderately Severe": f"Your PHQ-8 score of {score} indicates moderately severe depression. Please seek professional help from a mental health provider soon.",
            "Severe": f"Your PHQ-8 score of {score} suggests severe depression. Immediate professional intervention is strongly recommended. Please reach out to a mental health professional or crisis helpline.",
        }
        
        return interpretations.get(severity, f"PHQ-8 score: {score}/27")
    
    def get_next_steps(self, severity: str) -> List[str]:
        """Get recommended next steps based on severity"""
        steps = {
            "Minimal": [
                "Continue monitoring your mental health",
                "Maintain healthy sleep, diet, and exercise habits",
                "Stay connected with friends and family",
                "Consider journaling or mindfulness practices"
            ],
            "Mild": [
                "Talk to a trusted friend, family member, or counselor",
                "Consider self-help resources or support groups",
                "Practice stress management techniques",
                "Monitor symptoms and seek help if they worsen"
            ],
            "Moderate": [
                "Schedule an appointment with a therapist or counselor",
                "Consider evidence-based treatments like CBT or therapy",
                "Discuss symptoms with your primary care doctor",
                "Reach out to support networks"
            ],
            "Moderately Severe": [
                "Seek professional help from a mental health provider within days",
                "Consider both therapy and medication evaluation",
                "Inform family members or close friends about your struggles",
                "Create a safety plan and emergency contacts"
            ],
            "Severe": [
                "Seek immediate professional help (within 24-48 hours)",
                "Contact a crisis helpline if you have thoughts of self-harm",
                "Inform family members or trusted individuals immediately",
                "Consider going to an emergency room if in crisis",
                "Do not wait - severe depression requires urgent care"
            ]
        }
        
        return steps.get(severity, ["Consult a mental health professional"])


if __name__ == "__main__":
    # Test the enhanced symptom detector
    detector = PHQ8SymptomDetector()
    
    test_cases = [
        "I feel great and motivated!",
        "I've been feeling exhausted and can't focus on anything lately",
        "I can't sleep, feel worthless, have no appetite, and cry every day. This has been going on for weeks.",
        "Lost all interest in things I used to enjoy. Feel empty and tired all the time.",
    ]
    
    print("=" * 80)
    print("ENHANCED PHQ-8 SYMPTOM DETECTION TEST")
    print("=" * 80)
    
    for test_text in test_cases:
        print(f"\n📝 INPUT: {test_text}")
        print("-" * 80)
        
        results = detector.analyze_symptoms(test_text)
        
        print(f"PHQ-8 SCORE: {results['total_score']}/27")
        print(f"SEVERITY: {results['severity']}")
        print(f"\nDETECTED SYMPTOMS ({len(results['detected_symptoms'])}):")
        
        for detail in results['symptom_details']:
            print(f"  • {detail}")
        
        print(f"\nCLINICAL INTERPRETATION:")
        print(f"  {detector.get_clinical_interpretation(results)}")
        
        print(f"\nRECOMMENDED NEXT STEPS:")
        for step in detector.get_next_steps(results['severity']):
            print(f"  • {step}")
        
        print("=" * 80)
