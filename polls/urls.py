from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create/', views.create_question, name='create'),
    path('<int:question_id>/update/', views.update_question, name='update_question'),
    path('<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('<int:question_id>/delete_choice/<int:choice_id>/', views.delete_choice, name='delete_choice'),
]