"""Run all tests."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("=" * 70)
print("SKOOLACH TEST SUITE")
print("=" * 70)
print()

# Import and run all test modules
test_modules = [
    'test_parser',
    'test_player',
    'test_room',
    'test_graphics',
]

failed = []
passed = []

for module_name in test_modules:
    print(f"\nRunning {module_name}...")
    print("-" * 70)
    try:
        module = __import__(module_name)
        # Run the module's main
        if hasattr(module, '__file__'):
            exec(open(module.__file__).read())
        passed.append(module_name)
    except Exception as e:
        print(f"[FAIL] {module_name} FAILED: {e}")
        failed.append(module_name)

print()
print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Passed: {len(passed)}/{len(test_modules)}")
print(f"Failed: {len(failed)}/{len(test_modules)}")

if failed:
    print(f"\nFailed tests: {', '.join(failed)}")
    sys.exit(1)
else:
    print("\n[SUCCESS] ALL TESTS PASSED!")
    sys.exit(0)
