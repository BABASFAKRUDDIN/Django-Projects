from django.urls import path

from . import views
app_name = 'questions'
urlpatterns = [
    path('', views.get_list_of_questions, name = 'get_list_of_questions'),
    path('create/', views.create_question, name = 'create_question'),
    path('<int:question_id>/delete/', views.delete_question, name = 'delete_question'),
    path('<int:question_id>/update/', views.update_question, name = 'update_question'),
    path('<int:question_id>/get/', views.get_question, name = 'get_question'),
]
