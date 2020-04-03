# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from . import views
from .models import Question

def get_list_of_questions(request):
    res = request.GET
    print(res)
    if res == {}:
        questions = Question.objects.all()
    elif  res.get('sort_by') == 'desc':
        questions = Question.objects.order_by('-text')
    else:
        questions = Question.objects.order_by('text')
    context = {'questions':questions}
    return render(request, 'get_list_of_questions.html', context)

def get_question(request,question_id):
    question = Question.objects.get(pk = question_id)
    context = {'question':question}
    return render(request, 'each_question_form.html', context)
    #return HttpResponse('get_question')
    
def create_question(request):
    if request.method=='GET':
        return render(request,'create_question_form.html')
    elif request.method=='POST':
        res = request.POST
        questions = Question(text = res['question'], answer = res['answer'])
        if res['question'] == '' or res['answer'] =='':
            return render(request, 'create_question_failure.html')
        else:
            questions.save()
            return render(request, 'create_question_success.html')

def update_question(request,question_id):
    #if request.method=='GET':
    #    return render(request,'create_question_form.html')
    if request.method=='POST':
        res = request.POST
        if not res['question'] and not res['answer']:
            return render(request, 'update_question_failure.html')
        else:
            question = Question.objects.get(pk = question_id)
            question.text, question.answer = res['question'],res['answer']
            question.save()
            return render(request, 'update_question_success.html')

def delete_question(request,question_id):
    if Question.objects.filter(pk = question_id):
        res = Question.objects.get(pk = question_id)
        res.delete()
        return render(request, 'delete_question_success.html')
    else:
        return render(request, 'delete_question_failure.html')    