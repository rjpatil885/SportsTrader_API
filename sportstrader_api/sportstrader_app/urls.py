from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.home, name='event'),
    path('detail-matchinfo/<str:event_id>/',views.match_info, name='detail-matchinfo'),    
    path('season_filter/',views.season_filter,name='season_filter/'),
    path('quantity_filter/',views.quantityFilter,name='quantity_filter/'),
    path('date_filter/',views.dateFilter,name='date_filter/'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
