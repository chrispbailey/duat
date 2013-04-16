# Duat - A lightweight django UAT feedback tool

This is a simple django application for embedding a lightweight feedback mechanism into you websites. 
It's intended primarily as an aid for user acceptance testing, much like [Google Feedback](http://www.google.com/tools/feedback/intl/en/learnmore.html). The backend leverages Django's admin module to provide its functionality.

## How to use it

Via the admin interface on the server you set up a 'Project'. 
Once done this will provide you with a single custom javascript file which you can embed into your website. 
Once embedded, the javascript will create a small feedback form on the bottom right of the page.
When the user elects to provide feedback they can select any elements on the page which will become highlighted (to indicate the problem areas). After the feedback is submitted, the server generates an image of the page (with highlighted elements) and records the url, user agent and time of submission. Site administrators can then easily view the issues as they come in. You can view the generated image or the html of the problem page.

## How it works

The web tool allows the user to highlight different elements on the page (by adding a specific class to those elements). 
This DOM is then sent to the server where PhantomJS is used to generate a static image of the page and the admin interface lets you view the full page contents.

## Installation

1. Install the [Django](https://www.djangoproject.com/) framework
1. Download and extract [PhantomJS](http://phantomjs.org/)
2. Checkout this repository.
3. Edit settings.py 
 * Setup your database as necessary
 * Edit the PHANTOMJS_EXECUTABLE path
4. Initalise the database (don't forget to setup an administrator)
    python manage.py syncdb
5. Run the server
    python manage.py runserver 8000

6. Now visit the admin page (e.g. http://localhost:8000/admin), log in using the admin details and start creating projects.
Each project will have an accompanying javascript url (e.g. http://localhost:8000/project/[project_name]/feedback.js) which you can embed into your website use to start generating feedback!
 
## Notes

Inspiration for this system originally came from [feedback.js](http://experiments.hertzen.com/jsfeedback/) but I found the canvas tainting in chrome to be a blocker for our requirements so I decided to implement a simpler system.
Tested with Django 1.4
