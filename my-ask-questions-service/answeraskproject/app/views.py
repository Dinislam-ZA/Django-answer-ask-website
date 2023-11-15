from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from app.models import Question, Answer


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def index(request):
    questions = Question.objects.get_new_questions().prefetch_related('tags')
    page = paginate(questions, request)
    return render(request, 'index.html', {'page':page, 'show_answer_button':True})


def best_question_list(request):
    questions = Question.objects.get_best_questions().prefetch_related('tags')
    page = paginate(questions, request)
    return render(request, 'index.html', {'page':page, 'show_answer_button':True})


def question_list_by_tag(request, tag_name):
    questions = Question.objects.get_questions_by_tag(tag_name).prefetch_related('tags')
    page = paginate(questions, request)
    return render(request, 'index.html', {'page':page, 'show_answer_button':True})


def new_question(request):
    return render(request, 'new_question.html')


def login_user(request):
    return render(request, 'login_user.html')


def reg_user(request):
    return render(request, 'register_user.html')


def user_settings(request):
    return render(request, 'settings.html')


def question(request, question_id):
    q = Question.objects.get_question_with_likes(pk=question_id)
    answers = Answer.objects.get_answer_by_question(question_id)
    page = paginate(answers, request)
    return render(request, 'question_page.html', {'question':q, 'page':page, 'show_answer_button':False})
