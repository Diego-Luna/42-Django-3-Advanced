from django.urls import path
from .views import ArticlesView, HomeView, LoginUserView

app_name = 'ex00'

urlpatterns = [
	path('articles/', ArticlesView.as_view(), name='articles'),
	path('', HomeView.as_view(), name='home'),
	path('login/', LoginUserView.as_view(), name='login'),
]
