from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django.urls import reverse

# Create your views here.

def show(request):
    if request.method == 'GET':
        book_obj = models.Book.objects.all().values('name','price','publish__name','author__name')
        return render(request, 'show.html',{'book_list':book_obj})

def add(request):
    if request.method == 'GET':
        publish_obj = models.Publish.objects.all()
        author_obj = models.Author.objects.all()
        return render(request, 'addbook.html',{'publish_list':publish_obj,'author_list':author_obj})
    elif request.method == 'POST':
        book_dict = request.POST.dict()
        print(book_dict)
        del book_dict['csrfmiddlewaretoken']
        models.Book.objects.create(
            name = book_dict['name'],
            price = book_dict['price'],
            publish_id= book_dict['publish']
        )
        book_id = models.Book.objects.get(name=book_dict['name']).id
        print(book_id)
        book_obj = models.Book.objects.get(id=book_id)
        print(book_obj)
        book_obj.author.add(int(book_id),int(book_dict['author']))


        return redirect('show')

# def dele(request,n):
#     # print(n)
#     models.Book.objects.filter(pk=n).delete()
#     return redirect('show')