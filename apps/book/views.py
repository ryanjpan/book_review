from django.shortcuts import render, redirect
from .models import Book, Review
from ..login.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages
# Create your views here.

def book(request):
    if not 'fname' in request.session:
        return redirect('/')
    context = {
    'reviews': Review.objects.all().order_by('-created_at')[0:3],
    'books': Book.objects.all()
    }
    return render(request, 'book/landing.html', context)

def addreview(request):
    if not 'fname' in request.session:
        return redirect('/')
    return render(request, 'book/addreview.html')

def insertreview(request):
    if request.method != 'POST':
        return redirect(reverse('book:book'))
    title = request.POST['title']
    author = request.POST['author']
    comment = request.POST['comment']
    rating = request.POST['rating']
    if len(title) < 1:
        messages.error('Title is empty')
        return redirect(reverse('book:addreview'))
    if len(author) < 1:
        messages.error('Author is empty')
        return redirect(reverse('book:addreview'))
    try:
        book = Book.objects.get(title=title, author=author)
    except:
        book = Book.objects.create(title=title, author=author)

    user = User.objects.get(id=request.session['id'])
    Review.objects.create(book=book, user=user, rating=rating, comment=comment)
    return redirect(reverse('book:book'))

def title(request, id):
    try:
        book = Book.objects.get(id=id)
    except:
        return redirect(reverse('book:book'))
    context = {
    'reviews': Review.objects.filter(book__id=id),
    'book': book
    }
    return render(request, 'book/book.html', context)
