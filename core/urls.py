from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('how-it-works/', views.how_it_works_view, name='how-it-works'),
    path('career-paths/', views.career_paths_view, name='career-paths'),
    path('resources/', views.resources_view, name='resources'),
    path('accounts/', include('accounts.urls')),
    path('career/', include('career.urls')),
    path('quiz/', include('quiz.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "ai-career-guidance-coach Admin"
admin.site.site_header = "AI-Career Guidance Coach"
admin.site.index_title = "Admin Dashboard"

