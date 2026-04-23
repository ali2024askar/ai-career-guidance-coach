from django.db import models


class UserProfile(models.Model):
    name          = models.CharField(max_length=120)
    age           = models.PositiveSmallIntegerField()
    email         = models.EmailField(unique=True)
    interest_text = models.TextField()                  # "I like art and technology"
    career        = models.ForeignKey(                  # AI sets this after matching
        'career.Career',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"