import json
from django.urls import reverse
from .models import InterestKeyword
from accounts.models import UserProfile
from django.shortcuts import redirect, render
from django.http import JsonResponse, StreamingHttpResponse


def _require_profile(request):
    """Return (profile, None) or (None, redirect_response)."""
    user_id = request.session.get('user_id')
    if not user_id:
        return None, redirect(reverse('accounts:signin'))
    try:
        return UserProfile.objects.get(pk=user_id), None
    except UserProfile.DoesNotExist:
        request.session.flush()
        return None, redirect(reverse('accounts:signin'))


def chat_view(request):
    profile, bail = _require_profile(request)
    if bail:
        return bail

    user_message = request.session.get('user_message', '')

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            profile.interest_text = user_message
            profile.analysis_result = ''
            profile.career = None
            profile.save()
            request.session['user_message'] = user_message
            return redirect(reverse('career:analyze'))

    return render(request, 'career/chat.html', {
        'profile': profile,
        'user_message': user_message,
        'keywords': InterestKeyword.objects.filter(active=True),
    })


def analyze_view(request):
    profile, bail = _require_profile(request)
    if bail:
        return bail

    if not profile.interest_text:
        return redirect(reverse('career:chat'))

    return render(request, 'career/analyze.html', {
        'profile': profile,
    })


def analyze_stream_view(request):
    """
    SSE endpoint — streams real progress as each analysis step completes.
    GET request, session-authenticated.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if not profile.interest_text:
        return JsonResponse({'error': 'No interest'}, status=400)

    def _sse(data):
        return f"data: {json.dumps(data)}\n\n"

    def event_stream():
        from src.career_analyzer import (
            MIN_INPUT_LENGTH, MAX_INPUT_LENGTH,
            _build_prompt, _call_openai, _parse_index,
        )
        from django.apps import apps
        Career = apps.get_model('career', 'Career')
       # simulate delay for better UX (ensures loading state is visible)
        text = profile.interest_text.strip()

        # ── Step 1: Validate input ─────────────────────
        yield _sse({"progress": 10, "label": "Validating your input..."})

        if len(text) < MIN_INPUT_LENGTH:
            yield _sse({"progress": 100, "error_type": "user",
                        "error_message": "That's a bit short! Tell us more about what excites you."})
            return
        if len(text) > MAX_INPUT_LENGTH:
            yield _sse({"progress": 100, "error_type": "user",
                        "error_message": f"Please keep your description under {MAX_INPUT_LENGTH} characters."})
            return

        # ── Step 2: Load careers ───────────────────────
        yield _sse({"progress": 25, "label": "Loading career paths..."})

        slugs = list(Career.objects.values_list('slug', flat=True))
        if not slugs:
            yield _sse({"progress": 100, "error_type": "system",
                        "error_message": "No career paths are available yet. Please try again later."})
            return

        # ── Step 3: Build prompt ───────────────────────
        yield _sse({"progress": 40, "label": "Preparing AI analysis..."})
        prompt = _build_prompt(slugs, text)

        # ── Step 4: Call OpenAI (the slow part) ────────
        yield _sse({"progress": 50, "label": "Consulting our AI advisor..."})
        response_text, api_error = _call_openai(prompt)

        if api_error:
            yield _sse({"progress": 100, "error_type": api_error["type"],
                        "error_message": api_error["message"]})
            return

        # ── Step 5: Parse response ─────────────────────
        yield _sse({"progress": 75, "label": "Interpreting results..."})
        matched_slug = _parse_index(response_text, slugs)

        if matched_slug is None:
            yield _sse({"progress": 100, "error_type": "user",
                        "error_message": "We couldn't match your interest to a career. "
                                         "Please describe a real hobby, skill, or topic you're curious about."})
            return

        # ── Step 6: Look up career ─────────────────────
        yield _sse({"progress": 85, "label": "Matching career path..."})
        career = Career.objects.filter(slug__iexact=matched_slug).first()

        if not career:
            yield _sse({"progress": 100, "error_type": "system",
                        "error_message": "The matched career was not found. Please try again."})
            return

        # ── Step 7: Save to profile ────────────────────
        yield _sse({"progress": 93, "label": "Saving your career match..."})
        profile.career = career
        profile.analysis_result = (
            f'Based on your interest in "{profile.interest_text}", '
            f'we\'ve matched you with the {career.title} career path.'
        )
        profile.save()

        # ── Done ───────────────────────────────────────
        yield _sse({"progress": 100, "label": "Done! Redirecting...",
                    "redirect": reverse('career:roadmap')})
    
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # disable nginx buffering
    return response


def reset_interest_view(request):
    profile, bail = _require_profile(request)
    if bail:
        return bail

    profile.progress.all().delete()
    profile.interest_text = ''
    profile.analysis_result = ''
    profile.career = None
    profile.save()
    request.session['user_message'] = ''
    return redirect(reverse('career:chat'))


def roadmap_view(request):
    profile, bail = _require_profile(request)
    if bail:
        return bail

    career = profile.career
    if not career:
        return redirect(reverse('career:chat'))

    roadmap_steps = []
    steps = list(career.steps.all())
    progress_by_step = {
        p.step_id: p
        for p in profile.progress.filter(step__career=career)
    }

    previous_passed = True
    for step in steps:
        progress = progress_by_step.get(step.pk)
        passed = bool(progress and progress.passed)
        unlocked = previous_passed
        roadmap_steps.append({
            'step': step,
            'passed': passed,
            'unlocked': unlocked,
            'resources': list(step.resources.all()),
        })
        previous_passed = previous_passed and passed

    return render(request, 'career/roadmap.html', {
        'profile': profile,
        'career': career,
        'roadmap_steps': roadmap_steps,
    })
