from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('authority.urls')),
    path('api/todos/', include('todos.urls')),

    path('api/expenses/', include('expenses.urls')),
    path('api/income/', include('income.urls')),
    path('api/userstats/', include('userstats.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'helpers.error_views.error_404'
handler500 = 'helpers.error_views.error_500'
