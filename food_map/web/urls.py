from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home-page'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('history', views.history, name='history'),
    path('about', views.about, name='about'),
    path('places', views.places, name='places'),
    path('news/<int:pk>', views.NewsView.as_view(), name='news_text'),
    path('places/<int:pk>', views.PlacesView.as_view(), name='places_info'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('favourite/<int:pk>', views.favourite_add, name='favourite_add'),
    path('add_history', views.add_history, name='add_history'),
    path('place/<str:tag_slug>', views.places, name='places_by_tag'),
]

