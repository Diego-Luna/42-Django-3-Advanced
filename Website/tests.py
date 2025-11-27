from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, UserFavouriteArticle


class TestFavouritesViewRequiresAuthentication(TestCase):
	"""Test that favourites view is only accessible by registered users"""
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass123')
		self.url = reverse('Website:favourites')
	
	def test_anonymous_user_cannot_access_favourites(self):
		"""Anonymous users should be redirected to login page"""
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
		self.assertIn('/login/', response.url)
	
	def test_authenticated_user_can_access_favourites(self):
		"""Authenticated users should access favourites view successfully"""
		self.client.login(username='testuser', password='testpass123')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Website/favourites.html')


class TestPublicationsViewRequiresAuthentication(TestCase):
	"""Test that publications view is only accessible by registered users"""
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass123')
		self.url = reverse('Website:publications')
	
	def test_anonymous_user_cannot_access_publications(self):
		"""Anonymous users should be redirected to login page"""
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
		self.assertIn('/login/', response.url)
	
	def test_authenticated_user_can_access_publications(self):
		"""Authenticated users should access publications view successfully"""
		self.client.login(username='testuser', password='testpass123')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Website/publications.html')


class TestPublishViewRequiresAuthentication(TestCase):
	"""Test that publish view is only accessible by registered users"""
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass123')
		self.url = reverse('Website:publish')
	
	def test_anonymous_user_cannot_access_publish(self):
		"""Anonymous users should be redirected to login page"""
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
		self.assertIn('/login/', response.url)
	
	def test_authenticated_user_can_access_publish(self):
		"""Authenticated users should access publish view successfully"""
		self.client.login(username='testuser', password='testpass123')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Website/publish.html')


class TestRegisteredUserCannotAccessRegisterForm(TestCase):
	"""Test that authenticated users cannot access registration form"""
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass123')
		self.url = reverse('Website:register')
	
	def test_anonymous_user_can_access_register_form(self):
		"""Anonymous users should access the registration form"""
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'Website/register.html')
	
	def test_authenticated_user_cannot_access_register_form(self):
		"""Authenticated users should be redirected away from registration"""
		self.client.login(username='testuser', password='testpass123')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)


class TestUserCannotAddDuplicateFavourite(TestCase):
	"""Test that a user cannot add the same article twice to favourites"""
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass123')
		self.author = User.objects.create_user(username='author', password='authorpass123')
		self.article = Article.objects.create(
			title='Test Article',
			author=self.author,
			synopsis='This is a test synopsis',
			content='This is test content'
		)
		self.client.login(username='testuser', password='testpass123')
	
	def test_user_can_add_article_to_favourites_once(self):
		"""User should be able to add an article to favourites for the first time"""
		url = reverse('Website:add_favourite', kwargs={'article_id': self.article.pk})
		response = self.client.post(url, {'article': self.article.pk})
		self.assertEqual(UserFavouriteArticle.objects.filter(
			user=self.user, 
			article=self.article
		).count(), 1)
	
	def test_user_cannot_add_same_article_to_favourites_twice(self):
		"""User should not be able to add the same article to favourites twice"""
		UserFavouriteArticle.objects.create(user=self.user, article=self.article)
		initial_count = UserFavouriteArticle.objects.filter(
			user=self.user, 
			article=self.article
		).count()
		self.assertEqual(initial_count, 1)
		
		url = reverse('Website:add_favourite', kwargs={'article_id': self.article.pk})
		response = self.client.post(url, {'article': self.article.pk})
		
		final_count = UserFavouriteArticle.objects.filter(
			user=self.user, 
			article=self.article
		).count()
		self.assertEqual(final_count, 1)
