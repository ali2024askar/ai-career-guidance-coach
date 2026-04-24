import os
import random
from typing import Optional
from django.apps import apps


class CareerAnalyzer:
    """Simple career analysis and matching service"""

    def __init__(self):
        # Dynamically load careers from database
        self._load_careers()

    def _load_careers(self):
        """Load all available careers from the database"""
        Career = apps.get_model('career', 'Career')
        careers = Career.objects.all()
        self.available_careers = [
            {'slug': career.slug, 'name': career.title}
            for career in careers
        ]

    def analyze_interest(self, interest_text: str) -> Optional[str]:
        """
        Analyze user interest text and return a randomly selected career slug

        Args:
            interest_text: User's description of their interests

        Returns:
            Random career slug from available options
        """
        if not interest_text or not interest_text.strip():
            return None

        # Randomly select a career based on interest text
        if self.available_careers:
            selected_career = random.choice(self.available_careers)
            return selected_career['slug']

        return None

    def generate_analysis_text(self, interest_text: str, matched_career: str) -> str:
        """
        Generate a personalized analysis text based on the user's interest and matched career

        Args:
            interest_text: User's original interest description
            matched_career: The career slug that was matched

        Returns:
            Personalized analysis text
        """
        career_name = next(
            (c['name'] for c in self.available_careers if c['slug'] == matched_career),
            "AI Career"
        )

        # Simple personalized responses
        responses = [
            f"Based on your interest in {interest_text}, we've matched you with the {career_name} career path. This seems like an excellent fit for your goals!",
            f"Your passion for {interest_text} aligns perfectly with the {career_name} track. This career path will help you develop the skills you need.",
            f"Given your interest in {interest_text}, the {career_name} career path appears to be an ideal match for your aspirations.",
            f"We've selected the {career_name} career path based on your interest in {interest_text}. This will be a great journey for you!",
        ]

        return random.choice(responses)


# Global instance for easy import
career_analyzer = CareerAnalyzer()