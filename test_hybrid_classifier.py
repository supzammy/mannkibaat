"""
Test the Two-Stage Hybrid Intent Classifier
"""

from hybrid_intent_classifier import HybridIntentClassifier


def test_hybrid_classifier():
    """Test the hybrid classifier with various inputs."""
    
    print("=" * 80)
    print("TWO-STAGE HYBRID INTENT CLASSIFIER TEST")
    print("Stage 1: Rules | Stage 2: ML (90% accurate)")
    print("=" * 80)
    print()
    
    classifier = HybridIntentClassifier(use_ml=True, ml_threshold=0.6)
    
    # Get stats
    stats = classifier.get_stats()
    print("📊 Classifier Configuration:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Test cases
    test_cases = [
        # Should be rejected (casual)
        ("bro what should i tell you", False, "casual"),
        ("lol idk what to write", False, "casual"),
        ("yaar kya bolu", False, "casual"),
        ("just testing this app", False, "casual"),
        
        # Should be rejected (too short)
        ("I'm okay", False, "short"),
        ("nothing much", False, "short"),
        
        # Should be rejected (question)
        ("what should i write here", False, "question"),
        
        # Should be rejected (neutral/no feelings)
        ("today i went to work and came back home", False, "neutral"),
        
        # Should be accepted (genuine feelings)
        ("I feel sad and tired most days", True, "genuine"),
        ("I'm struggling with anxiety and depression", True, "genuine"),
        ("Can't sleep, feeling exhausted and hopeless", True, "genuine"),
        ("I've been worried and stressed about everything", True, "genuine"),
        ("My mood is low and I have no energy to do anything", True, "genuine"),
        ("Feeling overwhelmed with panic attacks", True, "genuine"),
        
        # Edge cases
        ("I think I might be experiencing clinical depression", True, "genuine"),
        ("My mental health has been declining", True, "genuine"),
    ]
    
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for text, expected_valid, expected_type in test_cases:
        result = classifier.classify_intent(text)
        
        is_valid = result['is_valid']
        decision = result['final_decision']
        confidence = result['confidence']
        method = result['method']
        
        # Check if prediction matches expectation
        match = "✅" if is_valid == expected_valid else "❌"
        
        if is_valid == expected_valid:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{match} \"{text[:60]}...\"")
        print(f"   Expected: {'Accept' if expected_valid else 'Reject'} ({expected_type})")
        print(f"   Got: {'Accept' if is_valid else 'Reject'} ({decision}) - {confidence:.1%}")
        print(f"   Method: {method}")
        
        # Show both stages
        if result['stage1_result']:
            stage1 = result['stage1_result']
            print(f"   Stage 1 (Rules): {stage1['type']} - {stage1['is_valid']}")
        
        if result['stage2_result']:
            stage2 = result['stage2_result']
            print(f"   Stage 2 (ML): {stage2['intent']} - {stage2['confidence']:.1%}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total = passed + failed
    accuracy = (passed / total * 100) if total > 0 else 0
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    print(f"📊 Accuracy: {accuracy:.1f}%")
    print()
    
    if accuracy >= 90:
        print("🎉 EXCELLENT! Hybrid classifier performing well!")
    elif accuracy >= 80:
        print("✅ GOOD! Hybrid classifier working as expected!")
    else:
        print("⚠️ WARNING! Classifier needs improvement")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_hybrid_classifier()
