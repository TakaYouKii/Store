from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm()
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались ')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(ListView):
    paginate_by = 10
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class NewsView(DetailView):
    model = News
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin ,CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/'
    raise_exception = True


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})


# def index(request):
#     news = News.objects.all()
#
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)
#
#
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category,
#     }
#     return render(request, 'news/category_info.html', context)


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect('home')
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})



