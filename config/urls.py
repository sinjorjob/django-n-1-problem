from django.contrib import admin
from django.urls import path, include
from django.conf import settings # 追加
import debug_toolbar  # 追加

urlpatterns = [
    path('admin/', admin.site.urls),
]


# 追加
if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
