#for rendering
from django.shortcuts import render

#for Post QuerySet and ordering by published_date
from django.utils import timezone
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	#take request and render it using appropriate html file
	#'post' is name referring to post variable in function while inside HTML file 
    return render(request, 'blog/post_list.html', {'posts' : posts})

