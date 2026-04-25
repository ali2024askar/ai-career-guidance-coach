from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Career, RoadmapStep, Resource
from accounts.models import UserProfile


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


def _run_analysis(profile):
    """Analyse interest, assign a career, and save — one call only."""
    from src.career_analyzer import analyze_interest, generate_analysis_text

    matched_slug = analyze_interest(profile.interest_text)

    career = None
    if matched_slug:
        career = Career.objects.filter(slug__iexact=matched_slug).first()
    if not career:
        career = Career.objects.first()

    profile.career = career
    profile.analysis_result = generate_analysis_text(
        profile.interest_text,
        career.title if career else 'a career',
    )
    profile.save()


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
    })


def analyze_view(request):
    profile, bail = _require_profile(request)
    if bail:
        return bail

    if not profile.interest_text:
        return redirect(reverse('career:chat'))

    return render(request, 'career/analyze.html', {
        'profile': profile,
        'analysis_seconds': 15,
    })


def analyze_api_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    if not profile.interest_text:
        return JsonResponse({'error': 'No interest text'}, status=400)

    _run_analysis(profile)
    return JsonResponse({'redirect': reverse('career:roadmap')})


def reset_interest_view(request):
    profile, bail = _require_profile(request)
    if bail:
        return bail

    # Clear all progress — back to square one
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
    demo_mode = False
    if not career or not career.steps.exists():
        career = _get_demo_roadmap()
        demo_mode = True

    roadmap_steps = []
    if career:
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
        'demo_mode': demo_mode,
        'roadmap_steps': roadmap_steps,
    })


def _get_demo_roadmap():
    career = Career.objects.first()
    if not career:
        career, _ = Career.objects.get_or_create(
            slug='default-career',
            defaults={
                'title': 'Default Career Path',
                'description': 'A default career path when no others are available.',
            },
        )
    return career
