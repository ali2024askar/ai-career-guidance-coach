from collections import defaultdict
from collections import OrderedDict

from django.shortcuts import render

from career.models import Career, Resource


def home_view(request):
    careers = Career.objects.all()[:6]
    resources = Resource.objects.select_related('career').order_by('-id')[:4]
    return render(request, 'core/home.html', {
        'careers': careers,
        'resources': resources,
    })


def how_it_works_view(request):
    careers = Career.objects.all()[:6]
    return render(request, 'core/how_it_works.html', {
        'careers': careers,
    })


def career_paths_view(request):
    careers = Career.objects.all()
    return render(request, 'core/career_paths.html', {
        'careers': careers,
    })


# def resources_view(request):
#     resources = Resource.objects.select_related('career').order_by('-id')[:10]
#     return render(request, 'core/resources.html', {
#         'resources': resources,
#     })


def resources_view(request):
    # Step 1: define type priority (to maximize coverage)
    type_order = ['video', 'platform', 'article']

    grouped_resources = OrderedDict()

    # Step 2: loop by type first (ensures diversity)
    for r_type in type_order:
        resources = (
            Resource.objects
            .filter(type=r_type)
            .select_related('career')
            .order_by('-id')
        )

        for resource in resources:
            if resource.career not in grouped_resources:
                grouped_resources[resource.career] = resource

    # Step 3: fallback (in case some careers didn't get picked)
    remaining = (
        Resource.objects
        .select_related('career')
        .order_by('-id')
    )

    for resource in remaining:
        if resource.career not in grouped_resources:
            grouped_resources[resource.career] = resource

    return render(request, 'core/resources.html', {
        'grouped_resources': grouped_resources,
    })