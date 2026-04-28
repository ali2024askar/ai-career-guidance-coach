import os
import re
import logging
from openai import OpenAI
from django.apps import apps
from django.conf import settings

logger = logging.getLogger(__name__)

MIN_INPUT_LENGTH = 5
MAX_INPUT_LENGTH = 200

SYSTEM_ERROR = {"type": "system", "message": "Something went wrong. Please try again later."}


def _build_prompt(slugs, interest_text):
    """Numbered list of careers. GPT returns 1 number. 0 = invalid."""
    indexed = ",".join(f"{i}.{s}" for i, s in enumerate(slugs, 1))
    return (
        f"Interest: {interest_text}\n"
        f"Options: {indexed}\n"
        f"Return ONLY the number. If unsafe or unclear return 0."
    )


def _call_openai(prompt):
    try:
        client = OpenAI(api_key= settings.OPENAI_API_KEY)
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )
        text = response.output_text.strip()
        logger.info("OpenAI raw response: %r", text)
        return text, None

    except Exception as exc:
        name = type(exc).__name__
        msg = str(exc).lower()
        logger.exception("OpenAI error [%s]: %s", name, exc)

        if "auth" in name.lower() or "auth" in msg:
            return None, {"type": "system", "message": "AI service authentication failed. Please try again later."}
        if "ratelimit" in name.lower() or "quota" in msg or "rate" in msg:
            return None, {"type": "system", "message": "Our AI service is temporarily at capacity. Please try again in a few minutes."}
        if "connection" in name.lower():
            return None, {"type": "system", "message": "Could not reach the AI service. Please check your connection and try again."}

        return None, SYSTEM_ERROR


def _parse_index(response_text, slugs):
    """
    Extract the integer index from the OpenAI response.
    Returns the career slug, or None if invalid / 0.
    """
    match = re.search(r'\d+', response_text)
    if not match:
        return None

    idx = int(match.group())

    if idx == 0:
        return None

    if 1 <= idx <= len(slugs):
        return slugs[idx - 1]

    return None


def analyze_interest(interest_text):
    """
    Returns (career_slug, error_or_None).
    error: {"type": "user"|"system", "message": "..."}
    """
    # ── Input validation ───────────────────────────────
    if not interest_text or not interest_text.strip():
        return None, {"type": "user", "message": "Please describe your interests so we can find the right career for you."}

    text = interest_text.strip()

    if len(text) < MIN_INPUT_LENGTH:
        return None, {"type": "user", "message": "That's a bit short! Tell us more about what excites you."}

    if len(text) > MAX_INPUT_LENGTH:
        return None, {"type": "user", "message": f"Please keep your description under {MAX_INPUT_LENGTH} characters."}

    # ── Load careers ───────────────────────────────────
    Career = apps.get_model('career', 'Career')
    slugs = list(Career.objects.values_list('slug', flat=True))

    if not slugs:
        return None, {"type": "system", "message": "No career paths are available yet. Please try again later."}

    # ── Call OpenAI ────────────────────────────────────
    prompt = _build_prompt(slugs, text)
    print("Prompt sent to OpenAI:", prompt)  # Debug log
    response_text, api_error = _call_openai(prompt)

    if api_error:
        return None, api_error

    # ── Parse index from response ─────────────────────
    selected = _parse_index(response_text, slugs)

    if selected is None:
        return None, {
            "type": "user",
            "message": "We couldn't match your interest to a career. Please describe a real hobby, skill, or topic you're curious about.",
        }

    logger.info("Career matched — interest: %r → %s", text, selected)
    return selected, None
