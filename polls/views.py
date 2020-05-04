from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.urls import path
from .robot import RobotWork
#
count = 1
def index(request):
    page =0
    try:
        page = request.GET['page']
    except Exception as e:
        print(e)
    print("page", page)

    return render(
        request,
        'polls/templates/main.html',
        context={'page': page},
    )

def info(request):
    global count
    print("info work--------------------------------------------")
    count+=1
    latest_question_list=[str(count)]
    return render(
        request,
        'polls/templates/index.html',
        context={'latest_question_list': latest_question_list},
    )

def add(request):
    print("add work--------------------------------------------")
    latest_question_list=[str(count)]
    try:
        pk = request.POST['choice']
        print("pk", pk)
    except Exception as e:
        print(e)


    question_text="test"
    question =["1", "2","3"]
    return render(
        request,
        'polls/templates/add.html',
        context={'latest_question_list': latest_question_list,
                 'question_text': question_text,
                 "question":question},
    )

vote_result ={"1":0, "2":0, "3":0}
votes = 0

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

def vote(request):
    global vote_result, votes
    question = ["1", "2", "3"]
    try:
        pk=request.POST['choice']
        vote_result[pk]+=1

    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'polls/templates/vote.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        votes += 1
        print("VOTE OK-----------------------", vote_result)
        return render(request, 'polls/templates/results.html', {
            'question': question,
            "vote_result":vote_result,
            'error_message': "You didn't select a choice.",
        })

        # return HttpResponseRedirect(reverse('polls/templates:results', args=()))


def control(request):
    global vote_result, votes
    try:
        p=request.POST
        g = request.GET
        print("control", p, g)

    except (KeyError):
        pass

    return HttpResponse("ok")



cam = RobotWork()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video(request):
    try:
        # return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass