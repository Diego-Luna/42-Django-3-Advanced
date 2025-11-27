from django.views.generic import ListView, RedirectView, DetailView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Article, UserFavouriteArticle
from .forms import CustomUserCreationForm, ArticleForm, AddToFavouriteForm
from django.contrib.auth.models import User


class ArticlesView(ListView):
	model = Article
	template_name = 'Website/articles.html'
	context_object_name = 'articles'
	
	def get_queryset(self):
		return Article.objects.all().order_by('-created')


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
		return Article.objects.filter(author=self.request.user).order_by('-created')


class ArticleDetailView(DetailView):
	model = Article
	template_name = 'Website/details.html'
	context_object_name = 'article'
	pk_url_kwarg = 'pk'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['favourite_form'] = AddToFavouriteForm(
				article_id=self.object.pk,
				user=self.request.user
			)
		return context
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if request.user.is_authenticated:
			existing = UserFavouriteArticle.objects.filter(
				user=request.user,
				article=self.object
			).exists()
			
			if not existing:
				form = AddToFavouriteForm(
					request.POST,
					article_id=self.object.pk,
					user=request.user
				)
				if form.is_valid():
					favourite = form.save(commit=False)
					favourite.user = request.user
					favourite.save()
		return self.get(request, *args, **kwargs)


class FavouritesView(LoginRequiredMixin, ListView):
	template_name = 'Website/favourites.html'
	context_object_name = 'articles'
	login_url = 'Website:login'
	
	def get_queryset(self):
		return Article.objects.filter(userfavouritearticle__user=self.request.user)


class RegisterView(CreateView):
	model = User
	form_class = CustomUserCreationForm
	template_name = 'Website/register.html'
	success_url = reverse_lazy('Website:login')
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('Website:home')
		return super().dispatch(request, *args, **kwargs)


class PublishView(LoginRequiredMixin, CreateView):
	model = Article
	form_class = ArticleForm
	template_name = 'Website/publish.html'
	login_url = 'Website:login'
	success_url = reverse_lazy('Website:publications')
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
