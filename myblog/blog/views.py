
from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Q

import urllib.request
import json
import markdown

url = 'http://open.iciba.com/dsapi'
page = urllib.request.urlopen(url).read()
data = page.decode("UTF-8")

data_dict = json.loads(data)
Qoute = data_dict['content']


class IndexView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        context.update({'qoute': Qoute})
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []

        left_has_more = False
        right_has_more = False

        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'post.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(ArticleDetailView, self).get_object(queryset=None)
        post.text = markdown.markdown(post.text,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
            'qoute': Qoute
        })
        return context


class ArchivesView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'archives_lists'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )

    def get_context_data(self, **kwargs):
        context = super(ArchivesView, self).get_context_data(**kwargs)
        context.update({'qoute': Qoute})
        return context


class CategoryView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'category_lists'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context.update({'qoute': Qoute})
        return context


class TagView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'tag_lists'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'qoute': Qoute})
        return context

def about(request):
    qoute = Qoute
    return render(request, 'about.html', locals())

def archive(request):
    qoute = Qoute
    return render(request, 'archive.html', locals())

def tag(request):
    qoute = Qoute
    return render(request, 'tags.html', locals())
