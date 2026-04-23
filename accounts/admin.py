from django.contrib import admin
from django.urls import reverse
from .models import UserProfile
from django.utils.html import format_html


# ──────────────────────────────────────────────────────────
#  Inline: show the user's step progress inside UserProfile
# ──────────────────────────────────────────────────────────
class UserStepProgressInline(admin.TabularInline):
    # imported here to avoid circular imports
    from quiz.models import UserStepProgress
    model        = UserStepProgress
    extra        = 0
    readonly_fields = ('step', 'passed', 'score', 'done_at')
    can_delete   = False
    verbose_name = "step progress"
    verbose_name_plural = "step progress"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    # ── List view ────────────────────────────────────────
    list_display = (
        'name',
        'email',
        'age',
        'career_badge',
        'steps_done',
        'joined',
    )
    list_filter  = ('career__title', 'created_at')
    search_fields = ('name', 'email', 'interest_text')
    ordering     = ('-created_at',)
    date_hierarchy = 'created_at'

    # ── Detail view ──────────────────────────────────────
    readonly_fields = ('created_at', 'career_link', 'interest_preview')
    fieldsets = (
        ('personal info', {
            'fields': ('name', 'age', 'email')
        }),
        ('career match', {
            'fields': ('interest_preview', 'career', 'career_link'),
            'description': 'The AI reads the interest text and sets the career field.'
        }),
        ('meta', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    inlines = [UserStepProgressInline]

    # ── Custom columns ───────────────────────────────────
    @admin.display(description='career', ordering='career__title')
    def career_badge(self, obj):
        if not obj.career:
            return format_html('<span style="color:#9ca3af">—</span>')
        return format_html(
            '<span style="background:#eef2ff;color:#4338ca;padding:2px 10px;'
            'border-radius:999px;font-size:12px;font-weight:500">{}</span>',
            obj.career.title
        )

    @admin.display(description='steps done')
    def steps_done(self, obj):
        from quiz.models import UserStepProgress
        total  = obj.career.steps.count() if obj.career else 0
        passed = UserStepProgress.objects.filter(user=obj, passed=True).count()
        if total == 0:
            return format_html('<span style="color:#9ca3af">—</span>')
        pct   = int(passed / total * 100)
        color = '#16a34a' if pct == 100 else '#4f46e5' if pct > 0 else '#9ca3af'
        return format_html(
            '<span style="font-size:12px;color:{}">{}/{} ({}%)</span>',
            color, passed, total, pct
        )

    @admin.display(description='joined', ordering='created_at')
    def joined(self, obj):
        return obj.created_at.strftime('%d %b %Y')

    @admin.display(description='career link')
    def career_link(self, obj):
        if not obj.career:
            return '—'
        url = reverse('admin:career_careerpath_change', args=[obj.career.pk])
        return format_html('<a href="{}">{}</a>', url, obj.career.title)

    @admin.display(description='interest text')
    def interest_preview(self, obj):
        return format_html(
            '<div style="background:#f9fafb;border:1px solid #e5e7eb;'
            'border-radius:6px;padding:10px 14px;font-size:13px;'
            'max-width:600px;line-height:1.6">{}</div>',
            obj.interest_text or '—'
        )