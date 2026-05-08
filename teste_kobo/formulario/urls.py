
from django.urls import path

from formulario import views


urlpatterns = [
    path("", views.index, name="index"),
    path("webhook/kobo/", views.webhook_kobo, name="webhook")
]