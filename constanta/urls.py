from django.contrib import admin
from django.urls import path

from scores import views as scores

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scores/events/', scores.events),
    path('scores/events/<int:event_id>/history/', scores.score_history)
]
