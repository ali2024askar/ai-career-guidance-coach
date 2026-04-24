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


def resources_view(request):
    resources = Resource.objects.select_related('career').order_by('-id')[:10]
    return render(request, 'core/resources.html', {
        'resources': resources,
    })
