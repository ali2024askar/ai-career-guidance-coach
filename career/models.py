from django.db import models


class Career(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    TYPE_CHOICES = [
        ('platform', 'Platform'),
        ('course',   'Course'),
        ('video',    'Video'),
        ('article',  'Article'),
        ('book',     'Book'),
    ]
    ICON_MAP = {
        'platform': 'grid',
        'course':   'mortarboard',
        'video':    'play-circle',
        'article':  'file-text',
        'book':     'book',
    }

    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='resources')
    title  = models.CharField(max_length=200)
    url    = models.URLField(blank=True)
    type   = models.CharField(max_length=20, choices=TYPE_CHOICES, default='platform')

    @property
    def icon(self):
        return self.ICON_MAP.get(self.type, 'link')

    def __str__(self):
        return f"{self.title} ({self.career.title})"


class RoadmapStep(models.Model):
    career      = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='steps')
    order       = models.PositiveSmallIntegerField()
    week_label  = models.CharField(max_length=50)    # "Week 1"
    title       = models.CharField(max_length=200)   # "Learn design basics"
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ('career', 'order')

    def __str__(self):
        return f"{self.career.title} — {self.week_label}: {self.title}"