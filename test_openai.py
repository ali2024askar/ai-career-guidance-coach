#!/usr/bin/env python
"""
Test script for OpenAI Career Analyzer
Run this to test the integration (requires OPENAI_API_KEY in .env)
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from src.career_analyzer import career_analyzer

def test_career_analyzer():
    """Test the career analyzer with sample inputs"""

    test_cases = [
        "I love working with data and building machine learning models",
        "I'm interested in AI product management and strategy",
        "Data science and analytics excite me",
        "I want to be a software engineer focusing on AI",
    ]

    print("Testing Career Analyzer...")
    print("=" * 50)

    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{test_input}'")
        try:
            # Test career matching
            matched_slug = career_analyzer.analyze_interest(test_input)
            print(f"  Matched career: {matched_slug}")

            if matched_slug:
                # Test analysis text generation
                analysis = career_analyzer.generate_analysis_text(test_input, matched_slug)
                print(f"  Analysis: {analysis[:100]}...")
            else:
                print("  No career match found")

        except Exception as e:
            print(f"  Error: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == '__main__':
    test_career_analyzer()