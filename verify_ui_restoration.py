"""
UI Restoration Verification
Checks that the professional medical UI is properly restored
"""

print("="*80)
print("🏥 PROFESSIONAL MEDICAL UI VERIFICATION")
print("="*80)

import re

# Read app.py
with open('app.py', 'r') as f:
    app_content = f.read()

checks = {
    "✅ Clean white background": 'background-color: white' in app_content,
    "✅ Professional header color (#1a365d)": '#1a365d' in app_content,
    "✅ Professional button color (#2563eb)": '#2563eb' in app_content,
    "✅ Demo buttons REMOVED": 'st.button("😊 Feeling Good"' not in app_content,
    "✅ Demo checkbox REMOVED": 'use_mock = st.checkbox("Demo"' not in app_content,
    "✅ Example hints as TEXT (not buttons)": 'example-hints' in app_content,
    "✅ Clean typography styling": 'font-family: -apple-system' in app_content,
    "✅ Professional text area styling": '.stTextArea textarea' in app_content,
    "✅ Medical disclaimer present": 'disclaimer' in app_content and 'NOT a substitute' in app_content,
    "✅ Privacy notice present": 'privacy-note' in app_content,
}

print("\n📋 UI Elements Check:")
print("-" * 80)

passed = 0
failed = 0

for check, result in checks.items():
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status}: {check.split('✅ ')[1] if '✅' in check else check}")
    if result:
        passed += 1
    else:
        failed += 1

print("-" * 80)
print(f"\n📊 Results: {passed}/{len(checks)} checks passed")

if failed == 0:
    print("\n🎉 SUCCESS! Professional Medical UI fully restored")
    print("\n✨ Changes Applied:")
    print("   • Removed ugly colored demo buttons")
    print("   • Removed confusing demo checkbox")
    print("   • Applied clean white background")
    print("   • Professional dark blue header (#1a365d)")
    print("   • Clean button styling (#2563eb)")
    print("   • Example prompts as text hints (not buttons)")
    print("   • Professional medical typography")
    print("   • Proper contrast (dark text on white)")
else:
    print(f"\n⚠️  WARNING: {failed} checks failed")

print("\n" + "="*80)
print("🌐 App Status:")
print("="*80)

import subprocess
result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
if 'streamlit run app.py' in result.stdout:
    print("✅ Streamlit app is RUNNING")
    print("✅ URL: http://localhost:8501")
    print("\n🎯 Verify the following in your browser:")
    print("   • Clean white background")
    print("   • NO colored demo buttons")
    print("   • NO demo checkbox")
    print("   • Text hints below input field")
    print("   • Professional blue buttons")
    print("   • Clean medical disclaimer")
else:
    print("⚠️  Streamlit app not running")
    print("Run: .venv/bin/streamlit run app.py")

print("\n" + "="*80)
print("✅ VERIFICATION COMPLETE")
print("="*80)
