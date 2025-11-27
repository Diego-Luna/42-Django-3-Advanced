from django.urls import path
from .views import (
	ArticlesView, 
	HomeView, 
	LoginUserView, 
	LogoutUserView,
	PublicationsView, 
	ArticleDetailView,
	FavouritesView,
	RegisterView,
	PublishView,
	AddToFavouriteView
)

app_name = 'Website'

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('login/', LoginUserView.as_view(), name='login'),
	path('logout/', LogoutUserView.as_view(), name='logout'),
	path('register/', RegisterView.as_view(), name='register'),
	path('articles/', ArticlesView.as_view(), name='articles'),
	path('publications/', PublicationsView.as_view(), name='publications'),
	path('publish/', PublishView.as_view(), name='publish'),
	path('detail/<int:pk>/', ArticleDetailView.as_view(), name='detail'),
	path('favourite/<int:article_id>/', AddToFavouriteView.as_view(), name='add_favourite'),
	path('favourites/', FavouritesView.as_view(), name='favourites'),
]
