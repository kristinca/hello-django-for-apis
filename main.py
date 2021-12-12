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

