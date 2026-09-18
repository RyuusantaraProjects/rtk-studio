from django.urls import path

from . import views, views_legal

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Public Legal Pages
    path("terms/", views_legal.terms_view, name="terms"),
    path("terms-of-service/", views_legal.terms_view, name="terms_of_service"),
    path("privacy/", views_legal.privacy_view, name="privacy"),
    path("privacy-policy/", views_legal.privacy_view, name="privacy_policy"),
    path("data-deletion/", views_legal.data_deletion_view, name="data_deletion"),
    path("panduan-penghapusan-data/", views_legal.data_deletion_view, name="panduan_penghapusan_data"),
]

