from django.views.generic import ListView, RedirectView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Article, UserFavouriteArticle


class ArticlesView(ListView):
	model = Article
	template_name = 'Website/articles.html'
	context_object_name = 'articles'


class HomeView(RedirectView):
	pattern_name = 'Website:articles'
	permanent = False


class LoginUserView(LoginView):
	template_name = 'Website/login.html'
	redirect_authenticated_user = True
	
	def get_success_url(self):
		return reverse_lazy('Website:home')


class LogoutUserView(LogoutView):
	next_page = 'Website:home'


class PublicationsView(LoginRequiredMixin, ListView):
	model = Article
	template_name = 'Website/publications.html'
	context_object_name = 'articles'
	login_url = 'Website:login'
	
	def get_queryset(self):
		return Article.objects.filter(author=self.request.user)


class ArticleDetailView(DetailView):
	model = Article
	template_name = 'Website/details.html'
	context_object_name = 'article'
	pk_url_kwarg = 'pk'


class FavouritesView(LoginRequiredMixin, ListView):
	template_name = 'Website/favourites.html'
	context_object_name = 'articles'
	login_url = 'Website:login'
	
	def get_queryset(self):
		return Article.objects.filter(userfavouritearticle__user=self.request.user)
