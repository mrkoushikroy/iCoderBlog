from home import models
from django.shortcuts import redirect, render, HttpResponse
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPost = Post.objects.all()
    context={'allPost': allPost}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    allPost = Post.objects.all()
    post = Post.objects.filter(slug=slug).first()
    post.views= post.views +1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent = None)
    replies = BlogComment.objects.filter(post=post).exclude(parent = None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'post': post, 'allPost': allPost, 'comments':comments, 'user':request.user, 'replyDict':replyDict}
    # return HttpResponse(f'This is blogPost: {slug}')
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        parentSno = request.POST.get('parentSno')
        post = Post.objects.get(sno=postSno)
        if parentSno == '':
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, 'Comment posted successfully')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, 'Reply has been posted successfully')
        return redirect(f"/blog/{post.slug}")
        
