from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Count, Q
from .models import Question, Option, UserStepProgress


# ──────────────────────────────────────────────────────────
#  Inline: Options inside Question
# ──────────────────────────────────────────────────────────
class OptionInline(admin.TabularInline):
    model   = Option
    extra   = 4
    fields  = ('text', 'is_correct')
    ordering = ('id',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.validate_min = True
        return formset


# ──────────────────────────────────────────────────────────
#  Question admin
# ──────────────────────────────────────────────────────────
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    # ── List view ─────────────────────────────────────────
    list_display  = (
        'short_text',
        'step_link',
        'career_name',
        'option_count',
        'has_correct',
        'order',
    )
    list_filter   = ('step__career', 'step')
    search_fields = ('text', 'step__title', 'step__career__title')
    ordering      = ('step__career', 'step__order', 'order')
    list_select_related = ('step', 'step__career')

    # ── Detail view ───────────────────────────────────────
    fieldsets = (
        (None, {
            'fields': ('step', 'order', 'text'),
            'description': (
                'Assign this question to a roadmap step. '
                'Add answer options below — mark exactly one as correct.'
            ),
        }),
    )
    inlines = [OptionInline]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate(
                _options=Count('options', distinct=True),
                _correct=Count('options', filter=Q(options__is_correct=True)),
            )
        )

    # ── Custom columns ────────────────────────────────────
    @admin.display(description='question', ordering='text')
    def short_text(self, obj):
        text = obj.text[:70] + ('…' if len(obj.text) > 70 else '')
        return format_html('<span style="font-weight:500">{}</span>', text)

    @admin.display(description='step', ordering='step__order')
    def step_link(self, obj):
        url = reverse('admin:career_roadmapstep_change', args=[obj.step.pk])
        return format_html(
            '<a href="{}">{} — {}</a>',
            url, obj.step.week_label, obj.step.title
        )

    @admin.display(description='career', ordering='step__career__title')
    def career_name(self, obj):
        return format_html(
            '<span style="background:#eef2ff;color:#4338ca;padding:2px 9px;'
            'border-radius:999px;font-size:11px">{}</span>',
            obj.step.career.title
        )

    @admin.display(description='options', ordering='_options')
    def option_count(self, obj):
        return obj._options

    @admin.display(description='correct answer', boolean=False)
    def has_correct(self, obj):
        if obj._correct == 1:
            return format_html(
                '<span style="color:#16a34a;font-weight:500">{}</span>',
                '✔ set'
            )
        elif obj._correct == 0:
            return format_html(
                '<span style="color:#dc2626;font-weight:500">{}</span>',
                '✗ missing'
            )
        else:
            return format_html(
                '<span style="color:#d97706;font-weight:500">⚠ {} correct</span>',
                obj._correct
            )


# ──────────────────────────────────────────────────────────
#  UserStepProgress admin  (read-only results view)
# ──────────────────────────────────────────────────────────
@admin.register(UserStepProgress)
class UserStepProgressAdmin(admin.ModelAdmin):

    # ── List view ─────────────────────────────────────────
    list_display = (
        'user_name',
        'step_info',
        'career_name',
        'result_badge',
        'score',
        'done_at_fmt',
    )
    list_filter  = ('passed', 'step__career', 'step')
    search_fields = ('user__name', 'user__email', 'step__title')
    ordering      = ('-done_at',)
    date_hierarchy = 'done_at'
    list_select_related = ('user', 'step', 'step__career')

    # ── Read-only (no one should edit quiz results manually) ──
    readonly_fields = ('user', 'step', 'passed', 'score', 'done_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # ── Custom columns ────────────────────────────────────
    @admin.display(description='user', ordering='user__name')
    def user_name(self, obj):
        url = reverse('admin:accounts_userprofile_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.name)

    @admin.display(description='step', ordering='step__order')
    def step_info(self, obj):
        return format_html(
            '<span style="font-size:13px">{} — {}</span>',
            obj.step.week_label, obj.step.title
        )

    @admin.display(description='career', ordering='step__career__title')
    def career_name(self, obj):
        return obj.step.career.title

    @admin.display(description='result', ordering='passed')
    def result_badge(self, obj):
        if obj.passed:
            return '<span style="background:#f0fdf4;color:#15803d;border:1px solid #bbf7d0;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:500">&#10003; passed</span>'
        
        return '<span style="background:#fef2f2;color:#b91c1c;border:1px solid #fecaca;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:500">&#10007; failed</span>'

    @admin.display(description='completed', ordering='done_at')
    def done_at_fmt(self, obj):
        return obj.done_at.strftime('%d %b %Y, %H:%M')