from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('analyze/', views.analyze_view, name='analyze'),
    path('analyze/stream/', views.analyze_stream_view, name='analyze_stream'),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('roadmap/reset-interest/', views.reset_interest_view, name='reset_interest'),
]
