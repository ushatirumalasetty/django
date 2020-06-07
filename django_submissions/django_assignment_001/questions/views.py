from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def get_list_of_questions(request):
    questions_list=Question.objects.all()
    sort=request.GET.get("sort_by")
    if sort=="desc":
        questions_list=questions_list.order_by('-text')
    else:
        questions_list=questions_list.order_by('text')
    object_list={
        "questions_list":questions_list
    }
    return render(request,"get_list_of_questions.html",object_list)

def create_question(request):
    if request.method=="GET":
        return render(request,"create_question_form.html")
    elif request.method=="POST":
        q=request.POST["question"]
        a=request.POST["answer"]
        if (q!="" and a!=""):
            Question.objects.create(text=q ,answer=a)
            return render(request,"create_question_success.html")
        else:
            return render(request,"create_question_failure.html")

def get_question(request,question_id):
     obj=Question.objects.get(id=question_id)
     context={
         "obj":obj
        }
     return render(request,"each_question_form.html",context)

def update_question(request,question_id):
    obj=Question.objects.get(id=question_id)
    obj.text=request.POST["question"]
    obj.answer=request.POST["answer"]
    if (obj.text!="" and obj.answer!=""):
            obj.save()
            return render(request,"update_question_success.html")
    else:
            return render(request,"update_question_failure.html")

def delete_question(request,question_id):
    obj=Question.objects.get(id=question_id)
    if question_id ==obj.id:
        obj.delete()
        return render(request,"delete_question_success.html")
    else:
        return render(request,"delete_question_failure.html")
