from django.views.generic import ListView, RedirectView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Article


class ArticlesView(ListView):
	model = Article
	template_name = 'ex00/articles.html'
	context_object_name = 'articles'


class HomeView(RedirectView):
	pattern_name = 'ex00:articles'
	permanent = False


class LoginUserView(LoginView):
	template_name = 'ex00/login.html'
	redirect_authenticated_user = True
	
	def get_success_url(self):
		return reverse_lazy('ex00:home')
