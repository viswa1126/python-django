from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .forms import CreatePollForm
from .models import Poll


# Create your views here.


# For Register
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()
                print("user-created")
                return redirect('/login')

        else:
            messages.info(request, 'incorrect password')
            return redirect('/register')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def home(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CreatePollForm()

    form = CreatePollForm()
    context = {
        'form': form
    }
    return render(request, 'create.html', context)


def result(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll': poll
    }
    return render(request, 'result.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'invalid options')

        poll.save()

        return redirect('result', poll.id)

    context = {
        'poll': poll
    }
    return render(request, 'vote.html', context)


def delete(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        poll.delete()
        return redirect('/')
    context = {
        'poll': poll
    }
    return render(request, 'delete.html', context)
