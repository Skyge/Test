
from django.contrib.syndication.views import Feed
from .models import Article


class AllPostsRssFeed(Feed):
    title = "Django 博客"
    link = "/"
    description = "Django 博客演示"

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.text