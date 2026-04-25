from django.db import models
from django.templatetags.static import static


class Career(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    TYPE_CHOICES = [
        ('platform',      'Platform'),
        ('course',        'Course'),
        ('video',         'Video'),
        ('article',       'Article'),
        ('book',          'Book'),
        ('documentation', 'Documentation'),
        ('guide', 'Guide'),
    ]

    # Maps type → local static icon filename
    ICON_FILE_MAP = {
        'platform':      'images/resource-icons/platform.png',
        'course':        'images/resource-icons/course.png',
        'video':         'images/resource-icons/video.png',
        'article':       'images/resource-icons/article.png',
        'book':          'images/resource-icons/book.png',
        'documentation': 'images/resource-icons/documentation.png',
        'guide':         'images/resource-icons/guide.png',
    }

    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='resources')
    step = models.ForeignKey('RoadmapStep', null=True, blank=True, on_delete=models.CASCADE, related_name='resources')
    title  = models.CharField(max_length=200)
    url    = models.URLField(blank=True)
    type   = models.CharField(max_length=20, choices=TYPE_CHOICES, default='platform')
    logo_url = models.URLField(blank=True, help_text="Custom logo URL. Leave blank to use the default icon for this type.")

    @property
    def effective_logo_url(self):
        """Return custom logo_url if set, otherwise the local static icon for the type."""
        if self.logo_url:
            return self.logo_url
        icon_path = self.ICON_FILE_MAP.get(self.type, 'images/resource-icons/platform.png')
        return static(icon_path)

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