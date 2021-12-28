""" My notes and work from the book 'Django for APIs Build web APIs with Python and Django' by William S. Vincent """


# a back-end API can be consumed by ANY JavaScript front-end.

# an API can support multiple front-ends written in different languages and frameworks.

# JavaScript is used for web front-ends,
# Android apps require the Java programming language,
# iOS apps need the Swift programming language.

# With a traditional monolithic approach, a Django website cannot support these various front-ends.
# But with an internal API, all three can communicate with the same underlying database back-end.

# an API-first approach can be used both internally and externally.

# Django REST Framework


# Chapter 1: Web APIs

# every URL like https://python.org/about/ has three potential parts:
# a scheme - https
# a hostname - www.python.org
# an (optional) path - /about/

# the Transmission Control Protocol (TCP) provides reliable, ordered
# and error-checked delivery of bytes between two application.

# To establish a TCP connection between two computers:
# 1. The client sends a SYN asking to establish a connection
# 2. The server responds with a SYN-ACK acknowledging the request and passing a connection
# 3. The client sends an ACK back to the server confirming the connection.

# Once the TCP connection is established, the two computers can start communicating via HTTP.

# Create-Read-Update-Delete -> CRUD functionality
#
# Create <--------------------> POST
# Read <--------------------> GET
# Update <--------------------> PUT
# Delete <--------------------> DELETE

# A webpage consists of HTML, CSS, images, and more. But an endpoint is just a way to access data
# via the available HTTP verbs.

# a web API has endpoints which are URLs with a list of available actions (HTTP verbs) that expose data
# (typically in JSON, which is the most common data format these days and the default for Django REST Framework).

# an endpoint which returns multiple data resources is known as a collection.

# creating an API involves making a series of endpoints: URLs with associated HTTP verbs.

# HTTP is a request-response protocol between two computers that have an existing TCP connection.
# The computer making the requests is known as the client while the computer responding is known as the server.

# Every HTTP message consists of a status line, headers, and optional body data.
# For example, her is a sample HTTP message that a browser might send to request the Google homepage located
# at https://www.google.com.
#
# GET / HTTP/1.1
# Host: google.com
# Accept_Language: en-US

# The top line is known as the request line and it specifies the HTTP method to use (GET), the path
# (/), and the specific version of HTTP to use (HTTP/1.1).
# The two subsequent lines are HTTP headers: Host is the domain name and Accept_Language is
# the language to use, in this case American English. There are many HTTP headers18 available.

# Every HTTP message, whether a request or response, therefore has the following format:
#
# Response/request line
# Headers...
# (optional) Body

# Status Codes

# 2xx Success - the action requested by the client was received, understood, and accepted
# 3xx Redirection - the requested URL has moved
# 4xx Client Error - there was an error, typically a bad URL request by the client
# 5xx Server Error - the server failed to resolve a request

# the most common ones: 200 (OK), 201 (Created), 301 (Moved Permanently), 404 (Not Found), and 500 (Server Error).

# it worked (2xx), it was redirected somehow (3xx), the client made an error (4xx), or the server made an error (5xx).

# HTTP is that it is a stateless protocol.
# This means each request/response pair is completely independent of the previous one.
# There is NO STORED MEMORY of past interactions, which is known as STATE in computer science.

# Managing state is really, really important in web applications.
# State is how a website remembers that you’ve logged in and how an e-commerce site manages your
# shopping cart. It’s fundamental to how we use modern websites, yet it’s not supported on HTTP itself.

# Historically state was maintained on the server but it has moved more and more to the client,
# the web browser, in modern front-end frameworks like React, Angular, and Vue.

# HTTP is stateless:
# -> very good for reliably sending information between two computers
# -> bad at remembering anything outside of each individual request/response pair.

# REST

# REpresentational State Transfer (REST) is an approach to building APIs on top of the web, which means on
# top of the HTTP protocol.

# Every RESTful API:
# -> is stateless, like HTTP
# -> supports common HTTP verbs (GET, POST, PUT, DELETE, etc.)
# -> returns data in either the JSON or XML format.

# A web API is a collection of endpoints that expose certain parts of an underlying database.
# We control:
# -> the URLs for each endpoint
# -> what underlying data is available,
# -> what actions are possible via HTTP verbs.
# By using HTTP headers we can set various levels of authentication and permission too.


# Chapter 2: Library Website and API

# We CAN NOT build a web API with only Django Rest Framework;
# it always MUST be added to a project AFTER Django itself has been installed and configured.
# Django creates websites containing webpages,
# Django REST Framework creates web APIs which are
# a collection of URL endpoints containing available HTTP verbs that return JSON.

# __init__.py -> a Python way to treat a directory as a package; it is empty
# asgi.py -> Asynchronous Server Gateway Interface, a new option in Django 3.0+
# settings.py -> contains all the configuration for our project
# urls.py -> controls the top-level URL routes
# wsgi.py -> Web Server Gateway Interface and helps Django serve the eventual web pages
# manage.py executes various Django commands such as running the local web server or creating a new app.

# First app
# Each app has a __init__.py file identifying it as a Python package:
# admin.py -> a configuration file for the built-in Django Admin app
# apps.py -> a configuration file for the app itself
# migrations/ directory -> stores migrations files for database changes
# models.py -> where we define our database models
# tests.py -> for our app-specific tests
# views.py -> where we handle the request/response logic for our web app.
# + urls.py file within each app -> for routing.

# Each web page in traditional Django requires several files: a view, url, and template.
# BUT FIRST WE NEED A DATABASE MODEL.

# Models

# We created a new database model -> we need to create a migration file to go along with it.
# We could just type python manage.py makemigrations but if there were multiple apps with database changes,
# both would be added to the migrations file which makes debugging in the future more of a challenge.
# Keep your migrations files AS SPECIFIC AS POSSIBLE, ex. $ python manage.py makemigrations books

# Admin

# create a superuser account and update admin.py -> the books app is displayed
# -> start entering data into our new model via the built-in Django app

# Views

# views.py file controls how the database model content is displayed.
# make our template and configure our URLs

# URLs

# set up both the project-level urls.py file and then one within the books app.
# When a user visits our site they will first interact with the config/urls.py file.

# We use the empty string, '', for the books app route which means a user on the homepage will be
# redirected directly to the books app.

# The final step is to create our template file that controls the layout on the actual web page.

# Ultimately, our API will expose a single endpoint that lists out all books in JSON. So we will need
# a new URL route, a new view, and a new serializer file.

# create a dedicated api app -> even if we add more apps in the future, each app can contain the
# models, views, templates, and urls needed for dedicated webpages, but all API-specific files for
# the entire project will live in a dedicated api app.

# The api app will not have its own database models so there is no need to create a migration file
# and run migrate to update the database.

# URLs

# Adding an API endpoint is just like configuring a traditional Django app’s routes.
# First at the project-level we need to include the api app and configure its URL route.

# Views

# views.py file -> relies on Django REST Framework’s built-in generic class views.
# These deliberately mimic traditional Django’s generic class-based views in format, but
# they ARE NOT THE SAME THING.

# cURL

# Browsable API

# Chapter 3: todoAPI

# Models
# We update our model ----->
# 1. make a new migration file
# 2. sync the database with the changes each time.

# If we update the models in two different apps and then run python manage.py makemigrations
# the resulting single migration file would contain data ON BOTH APPS!!!
# That just makes debugging harder.
# Try to keep your migrations AS SMALL AS POSSIBLE.

# Django REST Framework has a lengthy list of implicitly set default settings.
# AllowAny means that when we set it explicitly,
# the effect is exactly the same as if we had no DEFAULT_PERMISSION_CLASSES config set.

# the implicit default settings are designed so that developers can jump in and start working quickly in a local
# development environment. The default settings ARE NOT appropriate for production.

# here we are just building an API -> we do not need to create any template files or traditional Django views.
# Instead we will update three files that are Django REST Framework specific to transform our
# database model into a web API: urls.py, views.py, and serializers.py.

# URLs
# they are the entry-point for our API endpoints.
# Just as in a traditional Django project, the urls.py file lets us configure the routing.

# Serializers
# 1. We started with a traditional Django project and app where we made a database model and added data.
# 2. we installed Django REST Framework and configured our URLs.
# 3. Now we need to transform our data, from the models, into JSON that will be outputted at the URLs =>
#             ----->  we need a serializer  <-----

# Django REST Framework ships with a powerful built-in serializers class that we can quickly extend

# id is created automatically by Django so we didn’t
# have to define it in our t o d o  model but we will use it in our detail view

# Views

# In traditional Django views are used to customize what data to send to the templates.
# In Django REST Framework views do the same thing but for our serialized data.

# we have two routes ---> two distinct views.

# We will use ListAPIView to display all todos and RetrieveAPIView to display a single model instance.

# Traditionally consuming an API was a challenge.
# There simply weren’t good visualizations for all the information contained in the body and header
# of a given HTTP response or request.
# Instead most developers used a command line HTTP client like cURL or HTTPie.
# In 2012, the third-party software product Postman41 was launched and it is now used by millions
# of developers worldwide who want a visual, feature-rich way to interact with APIs.

# Django REST Framework is that it ships with a powerful browsable API that we can use right away.
# If you find yourself needing more customization around consuming an API,
# then tools like Postman are available. But often the built-in browsable API is more than enough.


# Browsable API

# CORS (Cross-Origin Resource Sharing)

# Whenever a client interacts with an API hosted on a different domain (mysite.com vs yoursite.com)
# or port (localhost:3000 vs localhost:8000) there are potential security issues.
# Specifically, CORS requires the server to include specific HTTP headers that allow for the client
# to determine if and when cross-domain requests should be allowed.

# Our Django API back-end will communicate with a dedicated front-end that is located on a
# different port for local development and on a different domain once deployed.

# The easiest way to handle this–-and the one recommended by Django REST Framework
# is to use middleware that will automatically include the appropriate HTTP headers based on our settings.
# localhost:3000 ---> default port for React

# Tests


# wTodo React Front-end

# the techniques described here will also work with any other popular front-end framework including
# Vue, Angular, or Ember. They will even work with mobile apps for iOS or Android, desktop
# apps, or really anything else. The process of connecting to a back-end API is remarkably similar.

# Install Node

# Like pipenv for Python, npm makes managing and installing multiple software packages much simpler.

# start -> mock up the API data in a variable named list which is actually an array with three values.
# next-> load the list into our component’s state and then use the JavaScript array method to display all the items.


# Django REST Framework + React

# the API endpoint listing all todos is at http://127.0.0.1:8000/api/. So we need to issue a GET request to it.

# There are two popular ways to make HTTP requests:
# with the built-in Fetch API60 or with axios,which comes with several additional features.
# We will use axios in this example.
