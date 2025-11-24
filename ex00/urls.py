from django.urls import path
from .views import ArticlesView, HomeView, LoginUserView, PublicationsView, ArticleDetailView

app_name = 'ex00'

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('login/', LoginUserView.as_view(), name='login'),
	path('articles/', ArticlesView.as_view(), name='articles'),
	path('publications/', PublicationsView.as_view(), name='publications'),
	path('detail/<int:pk>/', ArticleDetailView.as_view(), name='detail'),
]
