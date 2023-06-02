from django.urls import path
from .views import CreateAndGetView, GetByIdAndPatchAndDeleteView

urlpatterns = [
    path("teams/", CreateAndGetView.as_view()),
    path("teams/<team_id>/", GetByIdAndPatchAndDeleteView.as_view()),
]
