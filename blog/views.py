from django.shortcuts import render, HttpResponse
from blog.models import Post

# Create your views here.
def blogHome(request):
    allPost = Post.objects.all()
    context={'allPost': allPost}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    allPost = Post.objects.all()
    post = Post.objects.filter(slug=slug).first()
    context={'post': post, 'allPost': allPost}
    # return HttpResponse(f'This is blogPost: {slug}')
    return render(request, 'blog/blogPost.html', context)