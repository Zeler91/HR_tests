from .models import UserProfile, Test, Question, Result
import json

# func convert incoming data to type: 
# {points:sum of points, {question name:[{answer name:sum of answers},...,{}]}...}

def make_stat(users, test):
    results = []
    total = {}
    total['points'] = 0
    questions = test.questions.all()
    if type(users) is UserProfile:
        dict_results = json.loads(Result.objects.get(user=users, test=test).data)
        results.append(dict_results)
    else:
        for user in users:
            dict_results = json.loads(Result.objects.get(user=user, test=test).data)
            results.append(dict_results)
    for q in questions:
        answers_dict = json.loads(q.answers)
        total[q.question] = []
        for key in answers_dict.keys():
            total[q.question].append({key:0})
        for r in results:
            if r[str(q.id)]:
                index = int(r[str(q.id)].split('_')[0]) - 1
                total['points'] += int(r[str(q.id)].split('_')[1])
                for k in total[q.question][index].keys():
                    total[q.question][index][k] += 1
    if (total['points'] % 100) >= 11 and (total['points'] % 100) <= 19:
        total['points'] = f"{total['points']} баллов"
    elif (total['points'] % 10) == 1:
        total['points'] = f"{total['points']} балл"
    elif (total['points'] % 10) > 1 and (total['points'] % 10) < 5:
        total['points'] = f"{total['points']} балла"
    else:
        total['points'] = f"{total['points']} баллов"
    return total