from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', ArticleHome.as_view(), name='home'),
    path('addpage/', create, name='add_page'),
    path('addstudents/', addstudents, name='add_students'),
    path('editstudents/', editstudents, name='edit_students'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/edit/<int:id>', edit, name='edit'),
    path('post/<slug:post_slug>/editscore/<int:id>', editscore, name='editscore'),
    path('post/<slug:post_slug>/delete/<int:id>', delete, name='delete'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('worktype/<slug:type_slug>/', ArticleWorktype.as_view(), name='type'),
    path('about/', About.as_view(), name='about'),
    path('students/', StudentsHome.as_view(), name='students'),
]
