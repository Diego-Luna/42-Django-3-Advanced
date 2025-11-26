from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Article, UserFavouriteArticle


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Username'
		self.fields['password1'].label = 'Password'
		self.fields['password2'].label = 'Confirm Password'


class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('title', 'synopsis', 'content')
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['title'].label = 'Title'
		self.fields['synopsis'].label = 'Synopsis'
		self.fields['content'].label = 'Content'


class AddToFavouriteForm(forms.ModelForm):
	class Meta:
		model = UserFavouriteArticle
		fields = ('article',)
	
	def __init__(self, *args, **kwargs):
		self.article_id = kwargs.pop('article_id', None)
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		if self.article_id:
			self.fields['article'].queryset = Article.objects.filter(id=self.article_id)
			self.fields['article'].initial = self.article_id
			self.fields['article'].widget = forms.HiddenInput()
