#for rendering
from django.shortcuts import render

#for Post QuerySet and ordering by published_date
from django.utils import timezone
from .models import Post

#for single post page handling and error for getting objects
from django.shortcuts import get_object_or_404

#for new post view
from .forms import PostForm

#for redirecting user to website
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	#take request and render it using appropriate html file
	#'post' is name referring to post variable in function while inside HTML file 
    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk): #post_detail with catch the pk variable passed via url
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post' : post})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST) #upon submission, data is stored in request.POST
		if form.is_valid():
			post = form.save(commit=False) #don't save yet since we are missing fields (below)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk) #redirects to post_detail view
			#return redirect('post_list')
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post) #pass in post object with pk number 
	return render(request, 'blog/post_edit.html', {'form':form})