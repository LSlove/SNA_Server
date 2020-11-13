from django.urls import path, re_path
from app import views
from django.conf.urls import url, include 
from web import settings
from django.contrib import admin
if settings.DEBUG: import debug_toolbar





urlpatterns = [
    #re_path(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    # path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('user/', views.user, name='user'),
    path('vendor_model/', views.vendor_model, name='vendor_model'),
    path('team/', views.team, name='team'),
    path('device/', views.equip_code, name='equip_codes'),
    path('interface/', views.interface, name='interface'),
    path('device_performance/', views.device_performance, name='device_performance'),
    path('traffic/', views.traffic, name='traffic'),
    path('cur_faults/', views.cur_faults, name='cur_faults'),
    path('faults_history/', views.faults_history, name='faults_history'),
    path('critical/', views.critical, name='critical'),
    path('user_register/', views.user_register, name='user_register'),


    path('user_code/user_change/<user_id>/', views.user_change, name='user_change'),
    path('user_code/user_delete/<user_id>/', views.user_delete, name='user_delete'),
    
    path('team_register/', views.team_register, name="team_register"),
    path('user_code/team_change/<user_id>/', views.team_change, name="team_change"),
    path('user_code/team_delete/<user_id>/', views.team_delete, name="team_delete"),
    path('device_register/', views.device_register, name="device_register"),
    path('equipment/device_change/<eq_ip>', views.device_change, name="device_change"),
    path('equipment/device_delete/<eq_ip>/', views.device_delete, name='device_delete'),
    path('vendor_model_register/', views.vendor_model_register, name='vendor_model_register'),
    path('code/vendor_model_change/<int:num>/', views.vendor_model_change, name='vendor_model_change'),
    path('code/vendor_model_delete/<int:num>/', views.vendor_model_delete, name='vendor_model_delete')
]

