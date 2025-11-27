from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


def login_form(request):
	"""Add login form to context for all templates"""
	return {
		'login_form': AuthenticationForm(),
		'LANGUAGE_CODE': request.LANGUAGE_CODE,
		'LANGUAGES': settings.LANGUAGES,
	}
