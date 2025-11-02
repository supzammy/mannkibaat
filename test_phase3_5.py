"""
Comprehensive test for Phase 3.5 Input Validation Module
Tests all validation types and smart responses
"""

from input_validator import InputValidator


def test_validation():
    """Test the InputValidator with various inputs."""
    validator = InputValidator()

    # Test cases organized by expected validation type
    test_cases = [
        # CASUAL - Should be rejected
        {
            "input": "bro what should i tell you",
            "expected_valid": False,
            "expected_type": "casual",
            "category": "Casual English",
        },
        {
            "input": "lol idk what to say",
            "expected_valid": False,
            "expected_type": "casual",
            "category": "Casual English",
        },
        {
            "input": "yaar kya bolu",
            "expected_valid": False,
            "expected_type": "casual",
            "category": "Casual Hindi",
        },
        {
            "input": "bhai pata nahi",
            "expected_valid": False,
            "expected_type": "casual",
            "category": "Casual Hindi",
        },
        {
            "input": "hey just testing this out",
            "expected_valid": False,
            "expected_type": "casual",
            "category": "Testing/Demo",
        },
        # QUESTION - Should be rejected
        {
            "input": "what should i write here",
            "expected_valid": False,
            "expected_type": "question",
            "category": "Non-descriptive Question",
        },
        {
            "input": "i don't know what to tell you",
            "expected_valid": False,
            "expected_type": "question",
            "category": "Non-descriptive Question",
        },
        # SHORT - Should be rejected
        {
            "input": "I'm okay",
            "expected_valid": False,
            "expected_type": "short",
            "category": "Too Short",
        },
        {
            "input": "nothing much",
            "expected_valid": False,
            "expected_type": "short",
            "category": "Too Short",
        },
        # NEUTRAL - Should be rejected (no feeling words)
        {
            "input": "Today I went to work and came back home for dinner",
            "expected_valid": False,
            "expected_type": "neutral",
            "category": "Neutral/No Feelings",
        },
        # GENUINE - Should be accepted
        {
            "input": "I feel tired and sad most days",
            "expected_valid": True,
            "expected_type": "genuine",
            "category": "Genuine Feelings",
        },
        {
            "input": "I'm struggling with anxiety and depression lately",
            "expected_valid": True,
            "expected_type": "genuine",
            "category": "Genuine Feelings",
        },
        {
            "input": "Can't sleep well, feeling exhausted and hopeless",
            "expected_valid": True,
            "expected_type": "genuine",
            "category": "Genuine Feelings",
        },
        {
            "input": "I've been worried and stressed about everything",
            "expected_valid": True,
            "expected_type": "genuine",
            "category": "Genuine Feelings",
        },
        {
            "input": "My mood has been low and I have no energy or motivation",
            "expected_valid": True,
            "expected_type": "genuine",
            "category": "Genuine Feelings",
        },
        {
            "input": "Feeling overwhelmed with work, can't concentrate or focus",
            "expected_valid": True,
            "expected_type": "genuine",
            "category": "Genuine Feelings",
        },
        {
            "input": "I'm happy and feeling great today, full of energy",
            "expected_valid": True,
            "expected_type": "genuine",
            "category": "Positive Feelings",
        },
    ]

    print("=" * 80)
    print("PHASE 3.5: INPUT VALIDATION MODULE TEST")
    print("=" * 80)
    print()

    passed = 0
    failed = 0
    results_by_category = {}

    for test in test_cases:
        user_input = test["input"]
        expected_valid = test["expected_valid"]
        expected_type = test["expected_type"]
        category = test["category"]

        # Run validation
        is_valid, validation_type, metadata = validator.validate_input(user_input)

        # Check results
        status = "✅ PASS" if is_valid == expected_valid else "❌ FAIL"
        type_match = (
            "✓" if validation_type == expected_type else f"✗ (got: {validation_type})"
        )

        if is_valid == expected_valid:
            passed += 1
        else:
            failed += 1

        # Store by category
        if category not in results_by_category:
            results_by_category[category] = []
        results_by_category[category].append(
            {
                "input": user_input,
                "status": status,
                "expected": f"{expected_valid}/{expected_type}",
                "actual": f"{is_valid}/{validation_type}",
                "type_match": type_match,
            }
        )

    # Print results by category
    for category, results in results_by_category.items():
        print(f"\n{'─' * 80}")
        print(f"📂 {category}")
        print(f"{'─' * 80}")
        for r in results:
            print(f'{r["status"]}: "{r["input"][:60]}..."')
            print(f'   Expected: {r["expected"]} | Actual: {r["actual"]} {r["type_match"]}')

    # Print summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    total = passed + failed
    pass_rate = (passed / total * 100) if total > 0 else 0
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    print(f"📊 Pass Rate: {pass_rate:.1f}%")
    print("=" * 80)
    print()

    # Test smart responses
    print("=" * 80)
    print("SMART RESPONSE SYSTEM TEST")
    print("=" * 80)
    print()

    response_types = ["casual", "question", "short", "neutral", "empty"]
    for resp_type in response_types:
        response = validator.get_smart_response(resp_type)
        print(f"📝 Response Type: {resp_type.upper()}")
        print(f"   Message: {response['message']}")
        print(f"   Examples: {response['examples'][:80]}...")
        print()

    # Test validation stats
    print("=" * 80)
    print("VALIDATION STATISTICS TEST")
    print("=" * 80)
    print()

    sample_text = "I feel sad, tired, and anxious. Can't sleep or eat properly."
    stats = validator.get_validation_stats(sample_text)
    print(f'Sample Text: "{sample_text}"')
    print(f"   Word Count: {stats['word_count']}")
    print(f"   Positive Feelings: {stats['positive_feelings']}")
    print(f"   Negative Feelings: {stats['negative_feelings']}")
    print(f"   Physical Symptoms: {stats['physical_symptoms']}")
    print(f"   Mental Descriptors: {stats['mental_descriptors']}")
    print(f"   Total Feeling Keywords: {stats['total_feeling_keywords']}")
    print(f"   Is Gibberish: {stats['is_gibberish']}")
    print()

    print("=" * 80)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_validation()
