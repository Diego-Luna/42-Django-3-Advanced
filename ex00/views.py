from django.views.generic import ListView, RedirectView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
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

class PublicationsView(LoginRequiredMixin, ListView):
	model = Article
	template_name = 'ex01/publications.html'
	context_object_name = 'articles'
	login_url = '/login/'
	
	def get_queryset(self):
		return Article.objects.filter(author=self.request.user)

class ArticleDetailView(DetailView):
	model = Article
	template_name = 'ex01/details.html'
	context_object_name = 'article'
	pk_url_kwarg = 'pk'