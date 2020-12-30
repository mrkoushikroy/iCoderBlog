from django.db.models import query
from blog.models import Post
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout

# Html pages requests
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
    if len(query)>78:
        allPost=Post.objects.none()
    else:
        allPostTitle = Post.objects.filter(title__icontains = query)
        allPostContent = Post.objects.filter(content__icontains = query)
        allPostAuthor= Post.objects.filter(author__icontains = query)
        allPost =  allPostTitle.union(allPostContent, allPostAuthor)
    if allPost.count() == 0:
        messages.error(request, 'No search result found')
         
    params = {'allPost':allPost, 'query':query}
    return render(request, 'home/search.html', params)


# Authenticate APIs

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # check for errornous input
        
        if len(username) !=6:
            messages.error(request, 'username must be of 6 characters')
            return redirect('home')
        if not username.isalnum():
            messages.error(request, 'username must be of 6 characters of alpha numeric')
            return redirect('home')

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'username already exists try diff username')
            return redirect('home')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'email already exists try different email')
            return redirect('home')


        #create user
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lastname
        myuser.mobile = mobile
        myuser.save()
        messages.success(request, 'Hoola your account has been created !')
        return redirect('home')

    else:
        return HttpResponse('404 not found')


def handleLogins(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'Hoola successfully logged in !')
            return redirect('home')
        else:
            messages.error(request, 'User invalid credentials !')
            return redirect('home')

    return HttpResponse('404 not found')

def handleLogout(request):
    logout(request)
    messages.success(request, 'Hoola successfully logged out !')
    return redirect('home')
    