"""
Test Enhanced PHQ-8 System with 300+ Keywords
Validates symptom detection, scoring, and clinical output
"""

from phq8_model import analyze_depression_risk
from phq8_symptom_detector import PHQ8SymptomDetector

def print_separator(char="=", length=80):
    print(char * length)

def test_enhanced_detection():
    """Test enhanced symptom detection with various inputs"""
    
    test_cases = [
        {
            "name": "Minimal Risk - Positive Input",
            "input": "I feel great and motivated! Life is good.",
            "expected_severity": "Minimal",
            "expected_score_range": (0, 4)
        },
        {
            "name": "Mild Depression - Some Symptoms",
            "input": "I've been feeling tired lately and having trouble sleeping sometimes.",
            "expected_severity": "Mild",
            "expected_score_range": (5, 9)
        },
        {
            "name": "Moderate Depression - Multiple Symptoms",
            "input": "I can't sleep, feel exhausted all the time, lost interest in hobbies, and can't concentrate on anything.",
            "expected_severity": "Moderate",
            "expected_score_range": (10, 14)
        },
        {
            "name": "Severe Depression - Multiple Severe Symptoms",
            "input": "I feel completely worthless and hopeless. I can't sleep, have no appetite, cry every day, and can't focus on anything. This has been going on for weeks.",
            "expected_severity": "Severe",
            "expected_score_range": (15, 27)
        },
        {
            "name": "Complex Case - Mixed Symptoms with Frequency",
            "input": "For the past few weeks, I've been feeling down nearly every day. I lost all interest in things I used to enjoy. I'm tired all the time and sleeping too much. I feel like a failure and can't concentrate.",
            "expected_severity": ["Moderate", "Moderately Severe"],
            "expected_score_range": (10, 19)
        },
        {
            "name": "Casual Chat - Should Still Work After Validation",
            "input": "hey bro just checking this out",
            "note": "This should be filtered by input validation before PHQ-8 analysis"
        }
    ]
    
    print_separator()
    print("ENHANCED PHQ-8 SYSTEM TEST")
    print("Testing 300+ Keyword Symptom Detection")
    print_separator()
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"\n📝 INPUT:\n{test['input']}\n")
        
        # Run analysis
        result = analyze_depression_risk(test['input'], use_mock=True)
        
        # Display results
        print(f"{'─'*80}")
        print(f"📊 RESULTS:")
        print(f"{'─'*80}")
        print(f"PHQ-8 Score:        {result['phq8_score']}/27")
        print(f"Severity Level:     {result['risk_level']}")
        print(f"Confidence:         {result['confidence_percent']}")
        print(f"\nDetected Symptoms:  {result.get('symptom_count', 0)}")
        
        if 'detected_symptoms' in result and len(result['detected_symptoms']) > 0:
            print(f"\n🔍 SYMPTOM BREAKDOWN:")
            for symptom in result['detected_symptoms']:
                print(f"  • {symptom}")
            
            print(f"\n📋 DETAILED SCORING:")
            for detail in result['symptom_details']:
                print(f"  • {detail}")
        
        print(f"\n💬 CLINICAL INTERPRETATION:")
        print(f"  {result['interpretation']}")
        
        print(f"\n🎯 RECOMMENDED NEXT STEPS:")
        for step in result.get('next_steps', []):
            print(f"  • {step}")
        
        # Validation
        if 'note' not in test:
            print(f"\n{'─'*80}")
            print(f"✓ VALIDATION:")
            print(f"{'─'*80}")
            
            score_in_range = test['expected_score_range'][0] <= result['phq8_score'] <= test['expected_score_range'][1]
            
            if isinstance(test['expected_severity'], list):
                severity_match = result['risk_level'] in test['expected_severity']
            else:
                severity_match = result['risk_level'] == test['expected_severity']
            
            if score_in_range and severity_match:
                print(f"✅ PASS - Score: {result['phq8_score']} (expected {test['expected_score_range'][0]}-{test['expected_score_range'][1]})")
                print(f"✅ PASS - Severity: {result['risk_level']} (expected {test['expected_severity']})")
                passed += 1
            else:
                print(f"❌ FAIL - Score: {result['phq8_score']} (expected {test['expected_score_range'][0]}-{test['expected_score_range'][1]})")
                print(f"❌ FAIL - Severity: {result['risk_level']} (expected {test['expected_severity']})")
                failed += 1
        else:
            print(f"\nℹ️  NOTE: {test['note']}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {passed/(passed+failed)*100:.1f}%")
    print(f"{'='*80}\n")
    
    return passed, failed


def test_keyword_coverage():
    """Test that enhanced keywords are working"""
    
    print_separator()
    print("KEYWORD COVERAGE TEST")
    print("Testing specific symptom keywords")
    print_separator()
    
    detector = PHQ8SymptomDetector()
    
    keyword_tests = [
        ("Anhedonia", "I lost all interest in things I used to enjoy", "anhedonia_keywords"),
        ("Depressed Mood", "I feel hopeless and depressed every day", "depressed_mood_keywords"),
        ("Sleep Problems", "I can't sleep and wake up at 3am every night", "sleep_keywords"),
        ("Fatigue", "I'm completely exhausted and drained all the time", "energy_keywords"),
        ("Appetite", "I have no appetite and force myself to eat", "appetite_keywords"),
        ("Worthlessness", "I feel worthless and like a complete failure", "worthlessness_keywords"),
        ("Concentration", "I can't concentrate or focus on anything", "concentration_keywords"),
        ("Psychomotor", "I'm restless and can't sit still", "psychomotor_keywords"),
    ]
    
    print()
    for symptom_name, test_text, keyword_attr in keyword_tests:
        keywords = getattr(detector, keyword_attr)
        matched_keywords = [kw for kw in keywords if kw in test_text.lower()]
        
        if matched_keywords:
            print(f"✅ {symptom_name}: {len(matched_keywords)} keywords matched")
            print(f"   Text: '{test_text}'")
            print(f"   Matched: {', '.join(matched_keywords[:3])}")
        else:
            print(f"❌ {symptom_name}: No keywords matched")
        print()
    
    # Total keyword count
    total_keywords = sum([
        len(detector.anhedonia_keywords),
        len(detector.depressed_mood_keywords),
        len(detector.sleep_keywords),
        len(detector.energy_keywords),
        len(detector.appetite_keywords),
        len(detector.worthlessness_keywords),
        len(detector.concentration_keywords),
        len(detector.psychomotor_keywords),
    ])
    
    print(f"{'─'*80}")
    print(f"TOTAL CLINICAL KEYWORDS: {total_keywords}")
    print(f"{'─'*80}\n")


if __name__ == "__main__":
    # Test keyword coverage
    test_keyword_coverage()
    
    # Test enhanced detection
    passed, failed = test_enhanced_detection()
    
    # Final message
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Enhanced PHQ-8 system is working correctly.")
    else:
        print(f"⚠️  {failed} test(s) failed. Review results above.")
