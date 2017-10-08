# *-* coding:utf8 *-*
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Article
from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    post = get_object_or_404(Article, pk=post_pk)
    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，
    # 因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post)
            # return render(request, './post.html')
        else:
            comment_list = Comment.post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, './post.html', context=context)
    return redirect(post)
# render(req,'df_user/login.html',context_instance=RequestContext(req))。
