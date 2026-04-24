from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Career, RoadmapStep, Resource
from accounts.models import UserProfile
from src.career_analyzer import career_analyzer


def _generate_analysis(profile):
    """Generate personalized analysis using OpenAI"""
    interest_text = profile.interest_text.strip()
    if not interest_text:
        return "Welcome! Please share your career interests so we can create a personalized roadmap for you."

    # Get the matched career slug
    matched_career_slug = career_analyzer.analyze_interest(interest_text)

    # Generate personalized analysis text
    if matched_career_slug:
        return career_analyzer.generate_analysis_text(interest_text, matched_career_slug)
    else:
        # Fallback if no specific match
        return f"Thanks for sharing your interest in {interest_text}. Based on this, we've created a personalized roadmap with key learning milestones."


def _assign_career(profile):
    """Assign career using OpenAI analysis"""
    if not profile.interest_text:
        return None

    # Use OpenAI to determine the best career match
    matched_slug = career_analyzer.analyze_interest(profile.interest_text)

    if matched_slug:
        # Find the career in database (case-insensitive)
        career = Career.objects.filter(slug__iexact=matched_slug).first()
        if career:
            return career

    # Fallback to first available career if no match or API error
    return Career.objects.first()


def _run_analysis(profile):
    profile.analysis_result = _generate_analysis(profile)
    profile.career = _assign_career(profile)
    profile.save()


def _get_demo_roadmap():
    # Return the first available career, or create a default if none exist
    career = Career.objects.first()
    if not career:
        career, _ = Career.objects.get_or_create(
            slug='default-career',
            defaults={
                'title': 'Default Career Path',
                'description': 'A default career path when no others are available.',
            }
        )
    return career


def chat_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse('accounts:signin'))

    try:
        profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        request.session.flush()
        return redirect(reverse('accounts:signin'))

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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse('accounts:signin'))

    try:
        profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        request.session.flush()
        return redirect(reverse('accounts:signin'))

    if not profile.interest_text:
        return redirect(reverse('career:chat'))

    return render(request, 'career/analyze.html', {
        'profile': profile,
        'analysis_seconds': 1,
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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse('accounts:signin'))

    try:
        profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        request.session.flush()
        return redirect(reverse('accounts:signin'))

    profile.interest_text = ''
    profile.analysis_result = ''
    profile.career = None
    profile.save()
    request.session['user_message'] = ''
    return redirect(reverse('career:chat'))


def roadmap_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse('accounts:signin'))

    try:
        profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        request.session.flush()
        return redirect(reverse('accounts:signin'))

    career = profile.career
    demo_mode = False
    if not career or not career.steps.exists():
        career = _get_demo_roadmap()
        demo_mode = True

    roadmap_steps = []
    if career:
        steps = list(career.steps.all())
        progress_by_step = {
            progress.step_id: progress
            for progress in profile.progress.filter(step__career=career)
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
