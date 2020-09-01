from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('electro/', include('electro_social.urls', namespace='electro')),
    path('electro/', include('django.contrib.auth.urls')),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),
    path('posts/', include('posts.urls')),
    path('groups/', include('groups.urls')),
    # redirect user detail
    path('user/<int:pk>', RedirectView.as_view(
    pattern_name='electro:detail', permanent=False), name='redirect'),
    # notifications system
    path('inbox/notifications/',include(notifications.urls, namespace='notifications')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
