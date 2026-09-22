import subprocess
import sys


TEST_FILES = [
    "tests/test_jailbreak_detector.py",
    "tests/test_pii_detector.py",
    "tests/test_risk_scorer.py",
    "tests/test_output_security.py",
    "tests/test_output_validator.py",
    "tests/test_rag_security.py",
]


def run_tests():

    print("\n==============================")
    print("AI SECURITY TEST SUITE")
    print("==============================\n")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            *TEST_FILES,
            "-v"
        ]
    )

    print("\n==============================")

    if result.returncode == 0:
        print("ALL SECURITY TESTS PASSED!")
    else:
        print("SOME SECURITY TESTS FAILED.")

    print("==============================")

    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())