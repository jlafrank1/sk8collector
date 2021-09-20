from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skates/', views.skates_index, name='skates'),
    path('skates/<int:skate_id>/', views.skate_detail, name='detail'),
    path('skates/create/', views.SkateCreate.as_view(), name='skate_create'),
    path('skates/<int:pk>/update/', views.SkateUpdate.as_view(), name='skate_update'),
    path('skates/<int:pk>/delete/', views.SkateDelete.as_view(), name='skate_delete'),
    path('skates/<int:skate_id>/add_maintenance', views.add_maintenance, name='add_maintenance'),
    # remove maintenance log
    # path('skates/<int:skate_id>/remove_maintenance', views.remove_maintenance, name='remove_maintenance'),
    path('skates/<int:skate_id>/assoc_place/<int:place_id>/', views.assoc_place, name='assoc_place'),
    path('skates/<int:skate_id>/remove_place/<int:place_id>/', views.remove_place, name='remove_place'),
    path('skates/<int:skate_id>/add_photo/', views.add_photo, name='add_photo'),
    path('places/', views.PlaceList.as_view(), name='place_list'),
    path('places/create/', views.PlaceCreate.as_view(), name='place_create'),
    path('places/<int:pk>', views.PlaceDetail.as_view(), name='place_detail'),
    path('places/<int:pk>/update', views.PlaceUpdate.as_view(), name='place_update'),
    path('places/<int:pk>/delete/', views.PlaceDelete.as_view(), name='place_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
]
