from django.db import models


class Question(models.Model):
    """
    One quiz question linked to a career RoadmapStep.
    Import RoadmapStep as a string to avoid circular imports.
    """
    step  = models.ForeignKey(
        'career.RoadmapStep',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text  = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:80]


class Option(models.Model):
    question   = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text       = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{'[correct] ' if self.is_correct else ''}{self.text[:60]}"


class UserStepProgress(models.Model):
    """Tracks whether a user passed the quiz for a given step."""
    user    = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        related_name='progress'
    )
    step    = models.ForeignKey(
        'career.RoadmapStep',
        on_delete=models.CASCADE
    )
    passed  = models.BooleanField(default=False)
    score   = models.PositiveSmallIntegerField(default=0)
    done_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'step')

    def __str__(self):
        return (
            f"{self.user.name} — {self.step.week_label}: "
            f"{self.step.title} — {'passed' if self.passed else 'failed'}"
        )