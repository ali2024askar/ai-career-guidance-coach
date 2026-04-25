import random
import logging

from django.apps import apps

logger = logging.getLogger(__name__)


def analyze_interest(interest_text):
    """
    Analyze user interest text and return a random career slug.
    Later this will call an external API.
    """
    if not interest_text or not interest_text.strip():
        return None

    Career = apps.get_model('career', 'Career')
    slugs = list(Career.objects.values_list('slug', flat=True))

    if not slugs:
        return None

    selected = random.choice(slugs)

    # Log the prompt that would be sent to an external API
    logger.info(
        "Career analysis request — interest: %r | available careers: %s | selected: %s",
        interest_text,
        slugs,
        selected,
    )
    return selected


def generate_analysis_text(interest_text, career_name):
    """
    Generate a personalised analysis blurb.
    Later this will be the external-API response.
    """
    templates = [
        "Based on your interest in \"{interest}\", we've matched you with the "
        "{career} career path. This seems like an excellent fit for your goals!",

        "Your passion for \"{interest}\" aligns perfectly with the {career} "
        "track. This career path will help you develop the skills you need.",

        "Given your interest in \"{interest}\", the {career} career path "
        "appears to be an ideal match for your aspirations.",

        "We've selected the {career} career path based on your interest in "
        "\"{interest}\". This will be a great journey for you!",
    ]
    return random.choice(templates).format(
        interest=interest_text,
        career=career_name,
    )
