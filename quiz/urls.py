from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('step/<int:step_id>/', views.step_quiz_view, name='step_quiz'),
]