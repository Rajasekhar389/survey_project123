from django.urls import path
from .views import survey_view, results_view

urlpatterns = [
    path('survey/<int:page>/', survey_view, name='survey'),
    path('results/', results_view, name='results'),
]
