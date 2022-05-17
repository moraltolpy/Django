import datetime

from django.core.paginator import Paginator
from django.db.models import Count,Sum

from .models import *

menu = [ {'title': "Шетел студенттердің санын енгізу", 'url_name': 'add_students'},
         {'title': "Шетел студенттердің санын өзгерту", 'url_name': 'edit_students'}]

class DataMixin:
    paginate_by = 20
    def get_user_context(self, **kwargs):
        context = kwargs
        students = Foreign_Students.objects.raw('SELECT MAX(f.id),f.author,au.id,au.username, time_update, au.first_name,'
                                             'au.last_name,f.students FROM article_foreign_students as f '
                                             'INNER JOIN auth_user as au ON f.aut_username=au.username GROUP BY f.author ')
        types = Worktype.objects.annotate(Count('article'))
        posts = Article.objects.raw('SELECT id,title,subject,author,'
                                    'time_create, time_update,aut_username FROM article_article')
        counts = Article.objects.raw('SELECT a.id,MIN(slug), author,AU.FIRST_NAME, AU.LAST_NAME,SUM(score) AS sum,round(AVG(score),2) AS avg,'
                                     'type_id,COUNT(title) AS total FROM article_article as a INNER JOIN AUTH_USER AS AU'
                                     ' ON AU.USERNAME==A.AUT_USERNAME GROUP BY author')
        counts_type = Article.objects.raw('SELECT id, aut_username,  author, MAX(time_update), type_id,SUM(score) AS sum,round(AVG(score),2) AS avg, '
                                          'COUNT(title) AS total, time_create FROM article_article GROUP BY author,type_id')
        user_menu = menu.copy()

        try:
            if(Foreign_Students.objects.get(aut_username=self.request.user.username)):
                user_menu.pop(0)
        except:
            if not self.request.user.is_authenticated:
                user_menu.pop(0)
                user_menu.pop(0)
            else:
                user_menu.pop(1)

        context['students'] = students
        context['menu'] = user_menu
        context['posts'] = posts
        context['counts'] = counts
        context['counts_type'] = counts_type
        context['types'] = types
        if 'type_selected' not in context:
            context['type_selected'] = 0

        return context
