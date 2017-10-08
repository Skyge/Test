from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
# from django.db.models import permalink

import markdown


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    abstract = models.CharField(max_length=200, blank=True)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    # author = models.ForeignKey(User, blank=True)

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title

    # @permalink
    def get_absolute_url(self):
        return reverse('blog:showpost', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.abstract:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])
            self.abstract = strip_tags(md.convert(self.text))[:54]

        super(Article, self).save(*args, **kwargs)

    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
