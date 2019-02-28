from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogPost


def paging(request, list, num):
    paginator = Paginator(list, num)
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    return posts


def home(request):
    blog_list = Blog.objects.all()

    posts = paging(request, blog_list, 3)

    return render(request, "home.html", {
        "posts": posts,
    })


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    return render(request, "detail.html", {
        "blog": blog,
    })


def create(request):
    blog = Blog()

    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()

    blog.save()

    return redirect('/blog/' + str(blog.id))


def search(request):
    post_list = Blog.objects.all()
    keyword = request.GET.get('keyword', '')

    if keyword:
        post_list = post_list.filter(title__icontains=keyword)

    posts = paging(request, post_list, 3)

    return render(request, "search.html", {
        'posts': posts,
        'keyword': keyword
    })


def new(request):
    # 입력된 내용을 처리 -> POST
    if request.method == 'POST':
        form = BlogPost(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()

            form.save()

            return redirect('home')

    # 빈 페이지 출력 -> GET
    else:
        form = BlogPost()

        return render(request, 'new.html', {
            'form': form,
        })


def delete(request, blog_id):
    post = Blog.objects.get(pk=blog_id)

    if request.method == 'POST':
        post.delete()

    return redirect('home')


def edit(request, blog_id):
    before = Blog.objects.get(pk=blog_id)

    if request.method == 'POST':
        form = BlogPost(request.POST, instance=before)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.title = form.cleaned_data['title']
            blog.body = form.cleaned_data['body']

            blog.save()

            return redirect('/blog/' + str(blog.id))

    form = BlogPost(instance=before)

    return render(request, 'new.html', {
        "form": form,
    })
