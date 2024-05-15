from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('student/dashboard/enroll/', views.enroll, name='enroll'),
    path('advisor_approve/', views.advisor_approve, name='advisor_approve'),
    path('advisor_deny/', views.advisor_deny, name='advisor_deny'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('advisor/dashboard/', views.advisor_dashboard, name='advisor_dashboard'),
    path('advisor/dashboard/<path:path>', views.redirect_to_media),
    path('administration/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('administration/dashboard/<path:path>', views.redirect_to_media),
    path('admin_approve/', views.admin_approve, name='admin_approve'),
    path('admin_deny/', views.admin_deny, name='admin_deny'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
