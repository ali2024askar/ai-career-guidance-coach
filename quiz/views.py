from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Question, Option, UserStepProgress
from accounts.models import UserProfile
from career.models import RoadmapStep


def step_quiz_view(request, step_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse('accounts:signin'))

    try:
        profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        request.session.flush()
        return redirect(reverse('accounts:signin'))

    if not profile.career:
        return redirect(reverse('career:chat'))

    try:
        step = RoadmapStep.objects.select_related('career').prefetch_related('questions__options').get(pk=step_id)
    except RoadmapStep.DoesNotExist:
        return redirect(reverse('career:roadmap'))

    career = profile.career
    if step.career_id != career.pk:
        return redirect(reverse('career:roadmap'))

    previous_steps = list(career.steps.filter(order__lt=step.order).order_by('order'))
    progress_by_step = {
        progress.step_id: progress
        for progress in profile.progress.filter(step__career=career)
    }
    unlocked = all(progress_by_step.get(prev.pk, None) and progress_by_step[prev.pk].passed for prev in previous_steps)
    progress = progress_by_step.get(step.pk)
    passed = bool(progress and progress.passed)

    if not unlocked:
        return redirect(reverse('career:roadmap'))

    questions = list(step.questions.all())
    message = None
    if request.method == 'POST':
        if not questions:
            passed = True
            score = 0
            message = 'This step has no quiz questions, so it is marked complete.'
        else:
            score = 0
            correct_total = 0
            for question in questions:
                option_id = request.POST.get(f'question_{question.pk}')
                if option_id:
                    try:
                        option = question.options.get(pk=option_id)
                    except Exception:
                        option = None
                else:
                    option = None
                if option and option.is_correct:
                    score += 1
                correct_total += 1

            passed = (score == correct_total) and correct_total > 0
            if passed:
                message = 'All answers are correct. Great work! Resources for this step are now unlocked.'
            else:
                message = 'Some answers were incorrect. Please review the step and try again before unlocking the resources.'

        UserStepProgress.objects.update_or_create(
            user=profile,
            step=step,
            defaults={
                'passed': passed,
                'score': score,
            }
        )

        if passed:
            return redirect(reverse('career:roadmap'))

    return render(request, 'quiz/step_quiz.html', {
        'profile': profile,
        'step': step,
        'questions': questions,
        'passed': passed,
        'message': message,
    })
