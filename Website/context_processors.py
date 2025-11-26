from django.contrib.auth.forms import AuthenticationForm


def login_form(request):
	"""Add login form to context for all templates"""
	return {
		'login_form': AuthenticationForm()
	}
