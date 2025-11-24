from django.urls import path
from .views import (
	ArticlesView, 
	HomeView, 
	LoginUserView, 
	LogoutUserView,
	PublicationsView, 
	ArticleDetailView,
	FavouritesView
)

app_name = 'Website'

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('login/', LoginUserView.as_view(), name='login'),
	path('logout/', LogoutUserView.as_view(), name='logout'),
	path('articles/', ArticlesView.as_view(), name='articles'),
	path('publications/', PublicationsView.as_view(), name='publications'),
	path('detail/<int:pk>/', ArticleDetailView.as_view(), name='detail'),
	path('favourites/', FavouritesView.as_view(), name='favourites'),
]
