"""
System Verification Script
Checks all components are working correctly
"""

import json
from hybrid_intent_classifier import HybridIntentClassifier

print("="*80)
print("🔍 MANNKIBAAT SYSTEM VERIFICATION")
print("="*80)

# 1. Check training data
print("\n📊 1. Training Data Check")
try:
    with open('data/intent_classification_data.json', 'r') as f:
        data = json.load(f)
    genuine_count = sum(1 for d in data if d["label"]==1)
    casual_count = sum(1 for d in data if d["label"]==0)
    print(f"   ✅ Total examples: {len(data)}")
    print(f"   ✅ Genuine: {genuine_count}")
    print(f"   ✅ Casual: {casual_count}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Check ML model files
print("\n🤖 2. ML Model Files")
try:
    import os
    model_path = "model/ensemble_intent/"
    if os.path.exists(model_path):
        files = os.listdir(model_path)
        print(f"   ✅ Model directory exists")
        for f in files:
            size = os.path.getsize(os.path.join(model_path, f))
            print(f"   ✅ {f}: {size/1024:.1f} KB")
    else:
        print(f"   ❌ Model directory not found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Test Hybrid Classifier
print("\n🧪 3. Hybrid Classifier Tests")
try:
    classifier = HybridIntentClassifier(use_ml=True, ml_threshold=0.6)
    
    test_cases = [
        ("bro what should i tell you", False, "casual"),
        ("lol testing", False, "casual"),
        ("I feel sad and hopeless", True, "genuine"),
        ("worried about everything all the time", True, "genuine"),
        ("I think I might have depression", True, "genuine"),
        ("nothing makes me happy anymore", True, "genuine"),
    ]
    
    passed = 0
    failed = 0
    
    for text, expected_valid, expected_reason in test_cases:
        result = classifier.classify_intent(text)
        is_correct = result['is_valid'] == expected_valid
        
        if is_correct:
            passed += 1
            status = "✅"
        else:
            failed += 1
            status = "❌"
        
        decision = "Accept" if result['is_valid'] else "Reject"
        print(f"   {status} \"{text[:35]}...\" → {decision}")
    
    print(f"\n   📊 Results: {passed}/{len(test_cases)} passed ({100*passed/len(test_cases):.0f}%)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# 4. Check classifier stats
print("\n📈 4. Classifier Configuration")
try:
    stats = classifier.get_stats()
    for key, value in stats.items():
        print(f"   • {key}: {value}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 5. App status check
print("\n🌐 5. Streamlit App Status")
try:
    import subprocess
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    if 'streamlit run app.py' in result.stdout:
        print("   ✅ Streamlit app is running")
        # Extract port info
        for line in result.stdout.split('\n'):
            if 'streamlit run app.py' in line:
                print(f"   ✅ Process active")
                break
        print("   ✅ URL: http://localhost:8501")
    else:
        print("   ⚠️  Streamlit app not detected")
        print("   Run: .venv/bin/streamlit run app.py")
except Exception as e:
    print(f"   ⚠️  Cannot check app status: {e}")

print("\n" + "="*80)
print("✅ SYSTEM VERIFICATION COMPLETE")
print("="*80)
print("\n🎯 Quick Test Commands:")
print("   • Test hybrid classifier: .venv/bin/python test_hybrid_classifier.py")
print("   • Start app: .venv/bin/streamlit run app.py")
print("   • View app: http://localhost:8501")
print()
