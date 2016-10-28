from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.urlresolvers import reverse


def index(request):
    if 'id' in request.session:
        return redirect(reverse('book:book'))
    return render(request, 'login/index.html')

def register(request):
    if request.method != 'POST':
        return redirect('/')
    postdata = {
    'fname': request.POST['fname'],
    'lname': request.POST['lname'],
    'email': request.POST['email'],
    'password': request.POST['pass'],
    'confirm': request.POST['pass2'],
    }
    result = User.objects.register(postdata)
    print result
    if 'error' in result:
        messages.error(request, result['error'])
    else:
        messages.success(request, 'Successfully added user')
    return redirect('/')

def login(request):
    result = User.objects.login(request.POST['email'], request.POST['pass'])
    if 'error' in result:
        messages.error(request, result['error'])
        return redirect('/')
    user = result['success']
    request.session['fname'] = user.first_name
    request.session['lname'] = user.last_name
    request.session['email'] = user.email
    request.session['id'] = user.id
    return redirect(reverse('book:book'))

def logout(request):
    request.session.clear()
    return redirect('/')
