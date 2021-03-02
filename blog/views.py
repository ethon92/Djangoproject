

from django.shortcuts import render, redirect, get_object_or_404
from .form import LoginForm, PostForm
from django.http import HttpResponse
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required




def user_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # user = authenticate(request, user=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('home')
            # 尋找先顯示成功登陸再導向首頁
        else:
            return redirect('/')
            # 尋找如何導向登錄頁
    else:
        return render(request, 'login.html', {'Form': LoginForm})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login/')
def post(request):
    Form = PostForm()
    if request.method == 'POST':
        Form = PostForm(request.POST)
        Form.save()
        return render(request, "Upload_done.html")
    else:
        return render(request, "upload.html", {'Form': Form})


def home(request):
    post = Post.objects.all().order_by("-created_at")
    paginator = Paginator(post, 5)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    current_page_number = posts.number
    page = [current_page_number-2, current_page_number-1, current_page_number, current_page_number+1, current_page_number+2, current_page_number+3]
    page_range = page
    if page_range[-1] < paginator.num_pages:
        page_range.insert(-1, '...')  # 在頁數還未到總頁數之間增加省略符號
    if page_range[0] > 2:
        page_range.insert(0, '...')  # 在頁數大於第二頁之間增加省略符號
    if page_range[-1] != paginator.num_pages:
        page_range.pop()  # 當list最後一項不等於總頁數時則捨棄

    #頁面小於六頁之前

    if current_page_number == 1:
        page_range = [current_page_number]
    if current_page_number == 1 and paginator.num_pages == 2:
        age_range = [current_page_number, current_page_number+1]
    if current_page_number == 1 and paginator.num_pages == 3:
        page_range = [current_page_number, current_page_number+1, current_page_number + 2]
    if current_page_number == 1 and paginator.num_pages == 4:
        page_range = [current_page_number, current_page_number+1, current_page_number+2, current_page_number + 3]
    if current_page_number == 1 and paginator.num_pages == 5:
        page_range = [current_page_number, current_page_number+1, current_page_number + 2, '...']
    if current_page_number == 2:
        page_range = [current_page_number - 1, current_page_number]
    if current_page_number == 2 and paginator.num_pages == 3:
        page_range = [current_page_number-1, current_page_number, current_page_number+1]
    if current_page_number == 2 and paginator.num_pages == 4:
        page_range = [current_page_number - 1, current_page_number, current_page_number+1, current_page_number + 2]
    if current_page_number == 2 and paginator.num_pages == 5:
        page_range = [current_page_number - 1, current_page_number, current_page_number+1, current_page_number+2, current_page_number + 3]
    if current_page_number == 3:
        page_range = [current_page_number - 2, current_page_number - 1, current_page_number]
    if current_page_number == 3 and paginator.num_pages == 4:
        page_range = [current_page_number-2, current_page_number-1, current_page_number, current_page_number+1]
    if current_page_number == 3 and paginator.num_pages == 5:
        page_range = [current_page_number-2, current_page_number-1, current_page_number, current_page_number+1, current_page_number+2]
    if current_page_number == 4:
        page_range = [current_page_number - 2, current_page_number - 1, current_page_number]
    if current_page_number == 4 and paginator.num_pages == 5:
        page_range = [current_page_number-2, current_page_number-1, current_page_number, current_page_number+1]
    if current_page_number == 5:
        page_range = ['...', current_page_number - 2, current_page_number - 1, current_page_number]


    #頁面等於六頁之後
    """
    if current_page_number == paginator.num_pages:
        page_range = ['...', current_page_number-1, current_page_number]  # 當頁面為總頁面時,list為前一頁與最後一頁
    if current_page_number == paginator.num_pages-1:
        page_range = ['...', current_page_number-2, current_page_number-1, current_page_number, current_page_number+1]#  當頁面為總頁面前一頁
    if current_page_number == 1:
        page_range = [current_page_number, current_page_number+1, current_page_number+2, '...']  #  當為第一頁時
    if current_page_number == 2:
        page_range = [current_page_number-1, current_page_number, current_page_number+1, current_page_number+2, '...']  # 當為第二頁時
    """

    # 加入第一頁和最後一頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
        #剩下第一頁會出現兩頁跟最後一頁會出現兩頁和多一頁

    return render(request, "home.html", {"posts": posts, "page_range": page_range})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    previous_post = Post.objects.filter(created_at__gt=post.created_at).first()
    next_post = Post.objects.filter(created_at__lt=post.created_at).last()
    return render(request, "post.html", {"post": post, "previous_post": previous_post, "next_post": next_post})


def delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('home')


def edit(request, pk):
    post_object = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        Form = PostForm(request.POST, instance=post_object)
        if Form.is_valid():
            Form.save()
            return render(request, "Upload_done.html")
    else:
        Form = PostForm(instance=post_object)
        return render(request, "upload.html", {'Form': Form})



