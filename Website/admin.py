from django.contrib import admin
from .models import Article, UserFavouriteArticle


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'created', 'synopsis')
	list_filter = ('author', 'created')
	search_fields = ('title', 'synopsis', 'content')
	readonly_fields = ('created',)


@admin.register(UserFavouriteArticle)
class UserFavouriteArticleAdmin(admin.ModelAdmin):
	list_display = ('user', 'article')
	list_filter = ('user',)
	search_fields = ('user__username', 'article__title')
