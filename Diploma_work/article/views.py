from django.contrib.auth import logout, login

from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Count, Max
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .utils import *

types = Worktype.objects.annotate(Count('article'))
user_menu = menu.copy()

class ArticleHome(DataMixin,ListView):
    model = Article
    success_url = reverse_lazy('home')
    template_name = 'article/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Бастапқы бет")
        return dict(list(context.items()) + list(c_def.items()))

class StudentsHome(DataMixin,ListView):
    model = Article
    success_url = reverse_lazy('home')
    template_name = 'article/students.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

class ShowPost(DataMixin, DetailView):
    model = Article
    template_name = 'article/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'].author)
        return dict(list(context.items()) + list(c_def.items()))

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Бет табылмады</h1>')

class ArticleWorktype(DataMixin, ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Worktype.objects.get(slug=self.kwargs['type_slug'])
        c_def = self.get_user_context(title='Ғылыми жұмыстың түрі-' + str(c.name),type_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

class About(DataMixin,ListView):
    model = Article
    success_url = reverse_lazy('home')
    template_name = 'article/about.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'article/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Тіркелу")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'article/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Кіру")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def editscore(request, id, post_slug):
        user_menu = menu.copy()
        if (request.user.is_staff or request.user.is_superuser):
            try:
                if (Foreign_Students.objects.get(aut_username=request.user.username)):
                    user_menu.pop(0)
                else:
                    user_menu.pop(1)

                article = Article.objects.get(id=id)
                if request.method == "POST":
                    if(int(request.POST.get("score")) > 100):
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                    elif(int(request.POST.get("score")) < 100):
                        article.score = request.POST.get("score")
                        article.save()
                        back = article.slug
                    return HttpResponseRedirect('/post/' + back)
                else:
                    return render(request, "article/editscore.html", {"po": article, 'types': types, 'menu': user_menu})
            except Article.DoesNotExist:
                return HttpResponseNotFound("/")
        else:
            return HttpResponseNotFound("/")

def create(request):
        user_menu = menu.copy()
        error = ''
        if (Foreign_Students.objects.get(aut_username=request.user.username)):
            user_menu.pop(0)
        else:
            user_menu.pop(1)
        if request.method == "POST":
            form = AddPostForm(request.POST)
            if form.is_valid():
                form.save()
                new_form = form.save(commit=False)
                new_form.author = request.user.last_name + " " + request.user.first_name
                new_form.aut_username = request.user.username
                items = Article.objects.all()
                for i in items:
                    sl = slugify(i.author)
                    if i.slug== sl:
                        authid = request.user.last_name + " " + request.user.first_name + " " + str(new_form.id);
                        break
                    else:    authid = request.user.last_name + " " + request.user.first_name;

                new_form.slug = slugify(authid)
                new_form.save()
                return redirect('home')

            else:
                error = 'Detected error '

        form = AddPostForm()
        data = {'form': form,
                'error': error,
                'types': types,
                'menu': user_menu}
        return render(request, 'article/addpage.html', data)

def edit(request, id, post_slug):
        user_menu = menu.copy()
        try:
            if (Foreign_Students.objects.get(aut_username=request.user.username)):
                user_menu.pop(0)
            else:
                user_menu.pop(1)
            article = Article.objects.get(id=id)
            if request.method == "POST":
                back = article.slug
                article.title = request.POST.get("title")
                article.subject = request.POST.get("subject")
                article.save()
                return HttpResponseRedirect('/post/' + back)
            else:
                return render(request, "article/edit.html", {"po": article, 'types': types, 'menu': user_menu})
        except :
            return HttpResponseRedirect('/')

def delete(request, id, post_slug):
        try:
            article = Article.objects.get(id=id, aut_username=request.user.username)
            article.delete()
            items = Article.objects.all()
            for i in items:
                if i.aut_username == request.user.username:
                    back = i.slug
                    break
            try:
                return HttpResponseRedirect('/post/' + back)
            except:
                return HttpResponseRedirect('/')
        except:
            return HttpResponseRedirect('/')

def editstudents(request):
        user_menu = menu.copy()
        try:
            user_menu.pop(0)
            students = Foreign_Students.objects.get(aut_username=request.user.username)
            if request.method == "POST":
                if (int(request.POST.get("students")) > 100):
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                elif (int(request.POST.get("students")) <= 100):
                    students.students = request.POST.get("students")
                    students.save()
                return HttpResponseRedirect('/students')
            else:
                return render(request, "article/editstudents.html", {"st": students, 'types': types, 'menu': user_menu})
        except :
            return HttpResponseRedirect('/students')

def addstudents(request):
        user_menu = menu.copy()
        error = 'Detected error '
        user_menu.pop(1)
        if request.method == "POST":
            form = AddStudentsForm(request.POST)

            if form.is_valid():
                form.save()
                new_form = form.save(commit=False)
                new_form.author = request.user.last_name + " " + request.user.first_name
                new_form.aut_username = request.user.username
                new_form.save()
                return redirect('students')
            else:
                error = 'Detected error '
        form = AddStudentsForm()
        data = {'form': form,
                'error': error,
                'types': types,
                'menu': user_menu}
        return render(request, 'article/addstudents.html', data)
