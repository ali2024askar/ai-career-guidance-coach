from django.db import models


class UserProfile(models.Model):
    name          = models.CharField(max_length=120, blank=True, default='')
    age           = models.PositiveSmallIntegerField()
    email         = models.EmailField(unique=True)
    password      = models.CharField(max_length=128, blank=True)
    interest_text = models.TextField(blank=True)
    analysis_result = models.TextField(blank=True)
    career          = models.ForeignKey(                  # AI sets this after matching
        'career.Career',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.email})"
        return self.email