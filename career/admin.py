from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Career, Resource, RoadmapStep


# ──────────────────────────────────────────────────────────
#  Inline: Resources inside CareerPath
# ──────────────────────────────────────────────────────────
class ResourceInline(admin.TabularInline):
    model   = Resource
    extra   = 1
    fields  = ('title', 'url', 'type', 'step', 'icon_preview')
    readonly_fields = ('icon_preview',)
    ordering = ('type', 'title')

    @admin.display(description='icon')
    def icon_preview(self, obj):
        if obj.pk:
            return format_html(
                '<img src="{}" style="width:28px;height:28px;border-radius:6px;">',
                obj.effective_logo_url,
            )
        return '—'


# ──────────────────────────────────────────────────────────
#  Inline: RoadmapSteps inside Career
# ──────────────────────────────────────────────────────────
class RoadmapStepInline(admin.StackedInline):
    model       = RoadmapStep
    extra       = 1
    fields      = ('order', 'week_label', 'title', 'description')
    ordering    = ('order',)
    show_change_link = True   # link to the step detail page (for quiz questions)


# ──────────────────────────────────────────────────────────
#  CareerPath admin
# ──────────────────────────────────────────────────────────
@admin.register(Career)
class CareerPathAdmin(admin.ModelAdmin):

    # ── List view ─────────────────────────────────────────
    list_display = (
        'title',
        'slug',
        'step_count',
        'resource_count',
        'user_count',
    )
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('title',)

    # ── Detail view ───────────────────────────────────────
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description'),
        }),
    )
    inlines = [RoadmapStepInline, ResourceInline]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate(
                _steps=Count('steps', distinct=True),
                _resources=Count('resources', distinct=True),
                _users=Count('users', distinct=True),
            )
        )

    # ── Custom columns ────────────────────────────────────
    @admin.display(description='steps', ordering='_steps')
    def step_count(self, obj):
        url = (
            reverse('admin:career_roadmapstep_changelist')
            + f'?career__id__exact={obj.pk}'
        )
        return format_html(
            '<a href="{}" style="font-weight:500">{} steps</a>',
            url, obj._steps
        )

    @admin.display(description='resources', ordering='_resources')
    def resource_count(self, obj):
        url = (
            reverse('admin:career_resource_changelist')
            + f'?career__id__exact={obj.pk}'
        )
        return format_html(
            '<a href="{}" style="color:#4f46e5">{} resources</a>',
            url, obj._resources
        )

    @admin.display(description='users matched', ordering='_users')
    def user_count(self, obj):
        url = (
            reverse('admin:accounts_userprofile_changelist')
            + f'?career__id__exact={obj.pk}'
        )
        return format_html(
            '<a href="{}" style="color:#0891b2">{} users</a>',
            url, obj._users
        )


# ──────────────────────────────────────────────────────────
#  Resource admin (standalone, also editable inside CareerPath)
# ──────────────────────────────────────────────────────────
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):

    list_display  = ( 'type_badge', 'title', 'career', 'step', 'url_link')
    list_filter   = ('type', 'career')
    search_fields = ('title', 'url')
    ordering      = ('career', 'type', 'title')
    list_select_related = ('career', 'step')

    fieldsets = (
        (None, {
            'fields': ('career', 'step', 'title', 'type', 'url', 'logo_url', 'icon_preview'),
        }),
    )
    readonly_fields = ('icon_preview',)



    @admin.display(description='icon preview')
    def icon_preview(self, obj):
        if not obj.pk:
            return 'Save to see preview'

        return format_html(
            '<div style="display:flex;align-items:center;gap:12px;">'
            '<img src="{}" style="width:48px;height:48px;border-radius:10px;">'
            '<span style="color:#6b7280;font-size:13px;">'
            'Auto-selected from <strong>type</strong>. '
            'Set a custom <em>logo URL</em> to override.'
            '</span></div>',
            obj.effective_logo_url,
        )

    @admin.display(description='type', ordering='type')
    def type_badge(self, obj):
        colors = {
            'platform':      ('#eef2ff', '#4338ca'),
            'course':        ('#f0fdf4', '#15803d'),
            'video':         ('#fff7ed', '#c2410c'),
            'article':       ('#f0f9ff', '#0369a1'),
            'book':          ('#fdf4ff', '#7e22ce'),
            'documentation': ('#fff7ed', '#9a3412'),
        }
        bg, fg = colors.get(obj.type, ('#f3f4f6', '#374151'))
        return format_html(
            '<img src="{}" style="width:18px;height:18px;border-radius:4px;vertical-align:middle;margin-right:6px;">'
            '<span style="background:{};color:{};padding:2px 9px;'
            'border-radius:999px;font-size:11px;font-weight:500">{}</span>',
            obj.effective_logo_url, bg, fg, obj.get_type_display()
        )

    @admin.display(description='URL')
    def url_link(self, obj):
        if not obj.url:
            return '—'
        short = obj.url[:50] + ('...' if len(obj.url) > 50 else '')
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, short)


# ──────────────────────────────────────────────────────────
#  RoadmapStep admin  (standalone — shows quiz link)
# ──────────────────────────────────────────────────────────
@admin.register(RoadmapStep)
class RoadmapStepAdmin(admin.ModelAdmin):

    list_display  = ('week_label', 'title', 'career', 'order', 'question_count')
    list_filter   = ('career',)
    search_fields = ('title', 'description', 'career__title')
    ordering      = ('career', 'order')
    list_select_related = ('career',)

    fieldsets = (
        (None, {
            'fields': ('career', 'order', 'week_label', 'title', 'description'),
        }),
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate(_questions=Count('questions'))
        )

    @admin.display(description='quiz questions', ordering='_questions')
    def question_count(self, obj):
        url = (
            reverse('admin:quiz_question_changelist')
            + f'?step__id__exact={obj.pk}'
        )
        count = obj._questions
        color = '#16a34a' if count > 0 else '#ef4444'
        return format_html(
            '<a href="{}" style="color:{}">{} question{}</a>',
            url, color, count, 's' if count != 1 else ''
        )