from django.db.models import query
from blog.models import Post
from django.shortcuts import render, HttpResponse
from home.models import Contact
from blog.models import Post
from django.contrib import messages

# Create your views here.
def home(request):
    allPost = Post.objects.all()
    context={'allPost': allPost}
    return render(request, 'home/home.html', context)
    # return HttpResponse('This is home')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['mobile']
        message = request.POST['message']
        print(name, email, phone, message)

        if len(name)<4 or len(email)<5 or len(phone)<10 or len(message)<10:
            messages.error(request, 'Please fill the contact form correctly')
        else:
            contact = Contact(name= name, email= email, phone= phone, message= message)
            contact.save()
            messages.success(request, 'Successfully sent')
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query= request.GET['query']
    allPost = Post.objects.filter(title__icontains = query)
    params = {'allPost':allPost}
    return render(request, 'home/search.html', params)