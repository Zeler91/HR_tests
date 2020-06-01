from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib import auth  
from django.http.response import HttpResponseRedirect  
from django.urls import reverse_lazy
from .models import UserProfile, Test, Question, Result
from .statistic import make_stat
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

def index(request):  
    context = {}  
    if request.user.is_authenticated:
        try:
            context['user_profile'] = UserProfile.objects.get(user=request.user)  
        except ObjectDoesNotExist:
            if request.user.is_superuser:
                return redirect('/admin')
            else:
                return render(request, 'sorry.html')
            
        if UserProfile.objects.get(user=request.user):
            context['username'] = request.user.username
            context['users'] = UserProfile.objects.all()
            context['tests'] = []
            for test in Test.objects.all():
                context['tests'].append({'test':test, 'users_in_test':0, "users_complete_test":0})
            context['active_tests'] = []
            context['completed_tests'] = []
            for user in context['users'] :
                for test in user.tests.all():
                    for t in context['tests']:
                        if t['test'] == test:
                            t['users_in_test'] += 1
                            if test.name in user.completed_tests:
                                t['users_complete_test'] += 1
                    if test.name not in user.completed_tests:
                        context['active_tests'].append({user:test})
                    else:
                        context['completed_tests'].append({user:test})  
            return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('app:login'))  
 
def login(request):  
    if request.method == 'POST':  
        form = AuthenticationForm(request=request, data=request.POST)  
        if form.is_valid():  
            auth.login(request, form.get_user())  
            return HttpResponseRedirect(reverse_lazy('app:index'))  
    else:  
        return render(request, 'login.html')  
  
def logout(request):  
    auth.logout(request)  
    return HttpResponseRedirect(reverse_lazy('app:login'))

def test(request, pk):
    current_test = Test.objects.get(pk=pk)
    if request.method == 'POST':
        if len(request.POST) > current_test.questions.count():
            completed_test = {}
            result_str = {}
            result_data = request.POST.copy()
            result_data.pop('csrfmiddlewaretoken')
            for key, l in result_data.lists():
                list_to_string = ''.join([f"{v}, " for v in l])
                result_str[key] = list_to_string[:-2] # delete space and comma in last element
            result_json = json.dumps(result_str)
            completed_test['data'] = result_data
            result = Result(user = UserProfile.objects.get(user=request.user), test = Test.objects.get(pk=pk), data = result_json)
            result.save()
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.completed_tests == '':
                user_profile.completed_tests = Test.objects.get(pk=pk).name
            else:
                user_profile.completed_tests += f', {Test.objects.get(pk=pk).name}'
            user_profile.save()
            return HttpResponseRedirect(reverse_lazy('app:index'))
        else:
            return render(request, 'sorry.html')
    else:
        test_data = {}
        user_profile = UserProfile.objects.get(user=request.user)
        test_data['test'] = Test.objects.get(pk=pk)
        if test_data['test'] not in user_profile.tests.all():
            return render(request, 'sorry.html')
        if test_data['test'].name in user_profile.completed_tests:
            return HttpResponseRedirect(reverse_lazy('app:user_result', args=[pk,request.user.id]))
        template = loader.get_template('test_blank.html')
        questions = Test.objects.get(pk=pk).questions.all()
        question_data = {}
        test_data['answers'] = []
        test_data['questions_id'] = {}
        for q in questions :
            test_data['answers'].append(json.loads(q.answers))
            question_data[q.question] = json.loads(q.answers)
            test_data['questions_id'].update({q.question: q.id})
        test_data['question_data'] = question_data
        return HttpResponse(template.render(test_data, request))

def test_creator(request):
    # incoming data type : question<int1>, answer<int1>_<int2>, answer_value<int1>_<int2>
    # <int1> - question index, <int2> - answer index
    if request.method == 'POST':
        test = [request.POST['name']]
        # convert data from html form to Question model
        # result is list like: ["name of the test", 
        # {question:name of the question, answer:value,... ,answer:value}, ..., {...}]
        for key, value in request.POST.items():
            if key.startswith('question'):
                test.insert((int(key[8:])), {'question':value})
            if key.startswith('answer') and key[6] != '_':
                answer_index = int(key.split('_')[0][6:])
                test[answer_index].update({value:0})
            if key.startswith('answer_value'):
                answer_index = int(key.split('_')[1][5:])
                answer_value_index = int(key.split('_')[2])
                values_list = list(test[answer_index].values())
                values_list[answer_value_index] = value
                i = 0
                for k in test[answer_index].keys():
                    test[answer_index][k] = values_list[i]
                    i += 1

        # create model with converted data
        test_data = Test(name = test[0])
        test_data.save()
        for element in test:
            if type(element) is dict:
                q = element.pop('question')
                answers = json.dumps(element)
                test_question = Question(question = q, answers = answers)
                test_question.save()
                test_data.questions.add(test_question)
        return HttpResponseRedirect(reverse_lazy('app:index'))
    else:
        context = {}
        context['username'] = request.user.username
        return render(request, 'test_creator.html', context)

def total(request, pk):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.super_user:
        return render(request, 'sorry.html')
    # total test statistic where test pk=pk:
    total_results = {}
    total_results['test'] = Test.objects.get(pk=pk)
    users_in_test = UserProfile.objects.filter(tests = Test.objects.get(pk=pk))
    # how much users finished test
    users_complete_test = UserProfile.objects.filter(completed_tests__icontains = total_results['test'])
    total_results['users_in_test'] = users_in_test.count()
    total_results['users_complete_test'] = users_complete_test.count()
    if users_in_test.count():
        total_results['complete_percent'] = round(users_complete_test.count()/users_in_test.count()*100)
    # view answers statistic
    stat = make_stat(users_complete_test, total_results['test']) 
    total_results['total_points'] = stat.pop('points')
    total_results['total'] = stat
    return render(request, 'total.html', total_results)
    

def user_result(request, pk, user_id):
    # test statistic for user where user id=user_id
    total_results = {}
    total_results['test'] = Test.objects.get(pk=pk)
    user = UserProfile.objects.get(id = user_id)
    stat = make_stat(user, total_results['test'])
    total_results['total_points'] = stat.pop('points')
    total_results['total'] = stat
    return render(request, 'user_result.html', total_results)