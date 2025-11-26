from django import template
from django.utils.html import escape
from datetime import datetime
from django.utils.timezone import now

register = template.Library()


@register.filter
def truncate_synopsis(text, length=20):
	"""Truncate text to specified length and add ellipsis"""
	if len(text) > length:
		return text[:length] + '...'
	return text


@register.filter
def time_since_publication(created_date):
	"""Calculate time since article was published"""
	current_time = now()
	delta = current_time - created_date
	
	days = delta.days
	seconds = delta.seconds
	hours = seconds // 3600
	minutes = (seconds % 3600) // 60
	
	if days > 0:
		return f"{days} day{'s' if days > 1 else ''} ago"
	elif hours > 0:
		return f"{hours} hour{'s' if hours > 1 else ''} ago"
	elif minutes > 0:
		return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
	else:
		return "just now"
