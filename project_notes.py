#1. python3 -m venve [venv_name]
#2. source [venve_name]/bin/activate
#3. python -m pip install --upgrade pip
#4. pipi install -r requirements.txt (which contains Django~=2.0.6)

django-admin startproject mysite .
#creates template django file structure in directory
# . at end tells script to install Django in current directory (. is shorthand for that)
# djg
# ├───manage.py
# ├───mysite
# │        settings.py
# │        urls.py
# │        wsgi.py
# │        __init__.py
# └───requirements.txt

#manage.py is a script that helps with management of the site. With it we will 
#be able (amongst other things) to start a web server on our computer without
#installing anything else.

#settings.py file contains the configuration of your website.

#urls.py contains list of patterns used by urlresolver

#sqlite3 is set up in mysites/setting.py
python manage.py migrate
#creates database for project (responsible for applying and unapplying migrations.)

python manage.py runserver
#starts web server at http://127.0.0.1:8000/

Post
--------
title
text
author
created_date
published_date

publish()

#https://docs.djangoproject.com/en/2.0/ref/models/fields/#field-types

#We use objects to represent real things (e.g. blog posts) and have object properties and methods
#to represent the objects in a program
#'models' are objects that are stored in databases

##Creating an Application
#python manage.py startapp [appname (blog)]
#creates new [appname] directoy for new application
#make sure to add 'appname' under INSTALLED_APPS list in mysite/settings.py to tell Django to use it
#now files in [appname] directory will contain models, tests, views, and other files for that app
# djg
# ├── blog
# │   ├── __init__.py
# │   ├── admin.py
# │   ├── apps.py
# │   ├── migrations
# │   │   └── __init__.py
# │   ├── models.py
# │   ├── tests.py
# │   └── views.py
# ├── db.sqlite3
# ├── manage.py
# ├── mysite
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   └── wsgi.py
# └── requirements.txt

#now define object for model in blog/models.py
#from django.db import models
#class Post (models.Model):
#subclass models.Model makes sure Post is Django Model so Django knows to save it in database
#add properties and methods for Post class here

python manage.py makemigration blog
#add new model/changes to database in a 'commit'
#responsible for creating new migrations based on the changes you have made to your models
#this creates new migration file for changes we just made

python manage.py migrate blog
#applies the changes to database
#now Post model is in database

#modify blog/admin.py to allow Django admin to add/edit/delete Post objects
#admin.site.register(Post) -- this allows model to be visiable on admin page

#python manage.py runserver
#but now we need to create superuser to modify posts
python manage.py createsuperuser
#allows you to create superuser for your website

##Set up cloud server to host web app
#make account on PythonAnywhere and access Bash on it
pip3.6 install --user pythonanywhere
#change <> for below!
pa_autoconfigure_django.py https://github.com/<your-github-username>/<my-first-blog>.git
python manage.py createsuperuser
#now access live website on the internet

#workflow: work on local setup to maek cahnges, push to GitHub, pull changes down to live Web server

#in Django, URLconf is set of patterns that Django will tr yto match the requested URL to find the correct view
#add new URL paths to mysite/urls.py to direct [url]/ requests to blog.urls
#create urls.py in blog directory and assign 'view' called 'post_list' to root URL
#This pattern will tell Django that views.post_list is the right place to go if someone enters your website at the 'http://127.0.0.1:8000/' address.
#now in blog/views.py, create a post_list function that renders parameter 'request' by rendering with blog/post_list.html
#this render function will look in local template/ folder and search for the html file to render content with


##DJango ORM and QuerySets

python manage.py shell
#enables you to access Django's interactive console (Python + Django lib)
from blog.models import Post
Post.objects.all()
#list of posts created

from django.contrib.auth.models import User
User.objects.all()
#return list of all users
me = User.objects.get(username='jchoys')
Post.objects.create(author=me, title='Sample title', text='Test')
#creates new Post object with parameters as inputs

Post.objects.all()
#returns list of Posts including the latest one made above

#You can also filter QuerySets by replacing all()w ith filter
Post.objects.filter(author=me)
#returns list of Post objects with author as me

Post.objects.filter(title__contains='title')
#__ is used by Django ORM to separate field names (title) and operations/filters (contains)

from django.utils import timezone
Post.objects.filter(published_date__lte=timezone.now())
#post we just added on console is not published yet so it doesn't have published_date yet
#lets fix this

post = Post.objects.get(title="Sample title")
post.publish()
#this publishes the post so that it has a published_date attribute

#we can also order objects
Post.objects.order_by('created_date')
#or reverse order
Post.objects.order_by('-created_date')

#finally we cal also combine QuerySets by chaining them together
Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


#so far we have Post model in models.py, post_list in views.py, and post_list.html in templates
#how do we get posts to display in HTML? take content (model saved in database) to display in template?
#we do this with 'views' that connect models and template

#import Post and timezone into blog/views.py
#create a QuerySet variable post that represents ordered list of Post objects inside post_list view function
posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#pass this post variable into the render function inside {} so it is {'posts' : posts}

#now access post_list.html and embed python code into html using {{}} for variables and {% code %} for code
# {% for post in posts %}
#     <div>
#         <p>published: {{ post.published_date }}</p>
#         <h1><a href="">{{ post.title }}</a></h1>
#         <p>{{ post.text|linebreaksbr }}</p>
#     </div>
# {% endfor %}



