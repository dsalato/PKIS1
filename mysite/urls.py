from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from . import settings

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('', RedirectView.as_view(url='/polls/', permanent=True)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)