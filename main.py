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


# Blog API

# our API endpoints will support CRUD from the beginning which Django REST Framework makes quite seamless to do.
# Our database model will have five fields: author, title, body, created_at, and updated_at.
# We can use Django’s built-in User model.

# Django REST Framework takes care of the heavy lifting of transforming our database models into a RESTful API.
# There are three main steps to this process:
#    1. urls.py file for the URL routes
#    2. serializers.py file to transform the data into JSON
#    3. views.py file to apply logic to each API endpoint .

# start with the URL routes for the actual location of the endpoints:
# ---> Update the project-level urls.py file ->>> a new api/v1/ route for our posts app.

# It is a good practice to always version your APIs—v1/, v2/, etc —since when you make a large
# change there may be some lag time before various consumers of the API can also update.
# That way you can support a v1 of an API for a period of time while also launching a new, updated v2
# and avoid breaking other apps that rely on your API back-end.

# Our only app at this point is posts we can include it directly here.
# For multiple apps in a project --> create a dedicated api app and then include all the other API url routes into it.

# The serializer not only transforms data into JSON, it can also specify which fields to include or exclude.
# In our case, we will include the id field Django automatically adds to database models
# but we will exclude the updated_at field by not including it in our fields.

# An underlying database model will have far more fields than what needs to be exposed.
# Django REST Framework’s powerful serializer class makes it extremely straightforward to control this.

# to radically change the behavior of a given API endpoint, all we have to do is UPDATE OUR GENERIC VIEW.
# This is the advantage of using a full-featured framework like Django REST Framework.


# Permissions

# Create a new user

# add log in to the browsable API
# Django REST Framework has a one-line setting to add log in and log out directly to the browsable API itself.
# Within the project-level urls.py file, add a new URL route that includes rest_framework.urls.
# The actual route specified can be anything we want; what matters is that rest_framework.urls is included somewhere.

# View-Level Permissions
# restrict API access to authenticated users. There are multiple places we could do this:
#    ---->>> project-level, view-level, or object-level <<<-----
# Adding a dedicated permission_classes to each view seems REPETITIVE
# if we want to set the same permissions setting across our entire API.

# Project-Level Permissions
# a much simpler and safer approach to set a strict permissions policy at the project-level
# and loosen it as needed at the view level.
# Django REST Framework ships with a number of built-in project-level permissions settings we can use, including:
# • AllowAny - any user, authenticated or not, has full access
# • IsAuthenticated - only authenticated, registered users have access
# • IsAdminUser - only admins/superusers have access
# • IsAuthenticatedOrReadOnly - unauthorized users can view any page, but only authenticated
# users have write, edit, or delete privileges

# Implementing any of these four settings requires updating the DEFAULT_PERMISSION_CLASSES
# setting and refreshing our web browser.

# We have now required all users to authenticate before they can access the API, but we can always
# make additional view-level changes as needed, too.

# Custom permissions

# We want only the author of a specific blog post to be able to edit or delete it; otherwise the
# blog post should be read-only. So the superuser account should have full CRUD access to the
# individual blog instance, but the regular user testuser should not.

# Internally, Django REST Framework relies on a BasePermission class from which all other permission
# classes inherit. That means the built-in permissions settings like AllowAny, IsAuthenticated,
# and others extend it.


# User Authentication

# authentication -the process by which a user can register for a new account, log in with it, and log out.
# HTTP is a stateless protocol so there is no built-in way to remember if a user is
# authenticated from one request to the next. Each time a user requests a restricted resource it must verify itself.

# Django REST Framework ships with four different built-in authentication options:
# basic, session, token, and default.
# + there are many more third-party packages that offer additional features like JSON Web Tokens (JWTs).

# Basic Authentication
# 1. Client makes an HTTP request
# 2. Server responds with an HTTP response containing a 401 (Unauthorized) status code
#    and WWW-Authenticate HTTP header with details on how to authorize
# 3. Client sends credentials back via the Authorization HTTP header
# 4. Server checks credentials and responds with either 200 OK or 403 Forbidden status code

# the authorization credentials sent are the unencrypted base64 encoded77 version of <username>:<password>.
# advantage ----> simplicity
# disatvantages --> on every single request the server must look up and verify the username and password (inefficient)
# ----->user credentials are being passed in clear text—not encrypted at all—over the internet ->>> INSECURE
# basic authentication should only be used via HTTPS, the secure version of HTTP.

# Monolithic websites, like traditional Django, have long used an alternative authentication scheme
# that is a combination of sessions and cookies - stateful approach because a record must be kept and maintained
# on both the server (the session object) and the client (the session ID):
# 1. A user enters their log in credentials (typically username/password)
# 2. The server verifies the credentials are correct and generates a session object that is then
# stored in the database
# 3. The server sends the client a session ID—not the session object itself—which is stored as a
# cookie on the browser
# 4. On all future requests the session ID is included as an HTTP header and, if verified by the
# database, the request proceeds
# 5. Once a user logs out of an application, the session ID is destroyed by both the client and server
# 6. If the user later logs in again, a new session ID is generated and stored as a cookie on the client.

# The default setting in Django REST Framework is a combination of Basic Authentication and Session Authentication.

# The advantage of this approach is that it is more secure ---> user credentials are only sent once,
# not on every request/response cycle as in Basic Authentication;
# ---> It is also more efficient : the server does not have to verify the user’s credentials each time,
# it just matches the session ID to the session object which is a fast look up.

# disadvantages:
# 1.a session ID is only valid within the browser where log in was performed;
# it will not work across multiple domains. This is an obvious problem when
# an API needs to support multiple front-ends such as a website and a mobile app.
# 2. session object must be kept up-to-date which can be challenging in large sites with multiple
# servers. How do you maintain the accuracy of a session object across each server?
# 3. the cookie is sent out for every single request, even those that don’t require authentication ---> inefficient.


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DO NOT USE a session-based authentication scheme for any API that will have multiple front-ends.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# Token Authentication
# Token-based authentication is stateless:
# 1. a client sends the initial user credentials to the server
# 2. a unique token is generated and then stored by the client as either a cookie or in local storage
# 3.this token is then passed in the header of each incoming HTTP request
# 4. the server uses it to verify that a user is authenticated. The server itself does not keep a record of the user,
# just whether a token is valid or not.

# Cookies vs localStorage
# Cookies are used for reading server-side information. They are smaller (4KB) in size and automatically
# sent with each HTTP request.
# LocalStorage is designed for client-side information. It is much larger (5120KB)
# and its contents are not sent by default with each HTTP request.

# Tokens stored in both cookies and localStorage are vulnerable to XSS attacks.
# The current best practice is to store tokens in a cookie with the httpOnly and Secure cookie flags.

# benefits: tokens are stored on the client,
# scaling the servers to maintain up-to-date session objects is no longer an issue.
# +++ tokens can be shared amongst multiple front-ends: the same token can represent a user on the website
# and the same user on a mobile app.
# The same session ID can not be shared amongst different front-ends, a major limitation.

# downside: tokens can grow quite large. A TOKEN CONTAINS ALL USER INFORMATION,
# not just an id as with a session id/session object set up. Since the token is sent on every request,
# managing its size can become a performance issue.

# HOW the token is implemented can vary.
# Django REST Frameworks’ User Authentication built-in TokenAuthentication80 is deliberately quite basic:
# 1. it does not support setting tokens to expire -- a security improvement that can be added.
# 2. It only generates one token per user, so a user on a website and then later a mobile app will use the same token.
# Since information about the user is stored locally,
# this can cause problems with maintaining and updating two sets of client information.

# JSON Web Tokens (JWTs)
# --> a new, enhanced version of tokens that can be added to Django REST Framework via several third-party packages.
# ----> have several benefits including the ability to generate unique client tokens and token expiration.
# ---> They can either be generated on the server or with a third-party service like Auth.
# ----> JWTs can be encrypted which makes them safer to send over unsecured HTTP connections.

# the safest bet for most web APIs is to use a token-based authentication scheme.
# JWTs are a nice, modern addition though they require additional configuration.

# Default Authentication
# use both methods -> they serve different purposes.
# Sessions are used to power the Browsable API and the ability to log in and log out of it.
# BasicAuthentication is used to pass the session ID in the HTTP headers for the API itself.

# Implementing token authentication
# We keep SessionAuthentication since we still need it for our Browsable API, but now use tokens
# to pass authentication credentials back and forth in our HTTP headers. We also need to add the
# authtoken app which generates the tokens on the server. It comes included with Django REST Framework

# the tokens are only generated after there is an API call for a user to log in.

# Endpoints
# we will use dj-rest-auth83 in combination with django-allauth to simplify things.

# dj-rest-auth

# User Registration
# user registration = sign up endpoint
# Traditional Django does not ship with builtin views or URLs for user registration
# and neither does Django REST Framework.

# the third-party package django-allauth comes with user registration + a number of additional features
# to the Django auth system such as socialauthentication via Facebook, Google, Twitter, etc.
# we add dj_rest_auth.registration from the dj-rest-auth package --> we have user registration endpoints

# The email back-end config is needed since by default an email will be sent when a new user is registered,
# asking them to confirm their account. Rather than also set up an email server, we will
# output the emails to the console with the console.EmailBackend setting.

# SITE_ID is part of the built-in Django “sites” framework, which is a way to host multiple
# websites from the same Django project.

# added new apps ---->>> update the database <<<-----
#  ---> add a new URL route for registration.

# Tokens


# Viewsets and Routers
# can speed-up API development. They are an additional layer of abstraction on top of views and URLs.
# The primary benefit is that a single viewset can replace multiple related views.
# A router can automatically generate URLs for the developer.
# In larger projects with many endpoints this means a developer has to write less code.

# User endpoints

# Traditional Django has a built-in User model class that we have already used in the previous
# chapter for authentication. So we do not need to create a new database model. Instead we just
# need to wire up new endpoints:
# 1. new serializer class for the model
# 2. new views for each endpoint
# 3. new URL routes for each endpoint.

# there are three different ways to reference the User model in Django.
#URL routes -> Make sure to import our new UserList, and UserDetail views.
# Then we can use the prefix users/ for each.

# Viewsets
# A viewset is a way to combine the logic for multiple related views into a single class.
# One viewset can replace multiple views.

# Routers
# work directly with viewsets to automatically generate URL patterns for us.
# adopt a single route for each viewset. So two routes instead of four URL patterns.

# Django REST Framework has two default routers: SimpleRouter95 and DefaultRouter. We will
# use SimpleRouter but it’s also possible to create custom routers for more advanced functionality.

#