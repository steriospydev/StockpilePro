from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('', include('apps.account.urls')),
    path('supplier/', include('apps.supplier.urls')),
    path('storehouse/', include('apps.storehouse.urls')),
    path('product/', include('apps.product.urls')),
    path('invoice/', include('apps.invoice.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
