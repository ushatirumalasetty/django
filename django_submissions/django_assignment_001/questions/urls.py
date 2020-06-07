from django.urls import path

from . import views

urlpatterns = [
    path("",views.get_list_of_questions),
    path("create/",views.create_question),
    path("<int:question_id>/get/",views.get_question),
    path("<int:question_id>/update/",views.update_question),
    path("<int:question_id>/delete/",views.delete_question)

]
