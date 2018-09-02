from django.shortcuts import render

def post_list(request):
	#take request and render it using appropriate html file
    return render(request, 'blog/post_list.html', {})

