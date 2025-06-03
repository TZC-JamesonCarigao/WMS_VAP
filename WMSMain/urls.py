from django.contrib import admin
from django.urls import path, include

# WMSMain/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('WMSApp.urls')),  # ✅ root points to WMSApp
]

