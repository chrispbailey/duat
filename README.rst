Duat - A lightweight django UAT feedback tool
=============================================

This is a simple django application for embedding a lightweight feedback
mechanism into you websites. It’s intended primarily as an aid for user
acceptance testing, much like `Google Feedback`_. The backend leverages
Django’s admin module to provide its functionality.

How to use it
-------------

Via the admin interface on the server you set up a ‘Project’. Once done
this will provide you with a single custom javascript file which you can
embed into your website. Once embedded, the javascript will create a
small feedback form on the bottom right of the page. When the user
elects to provide feedback they can select any elements on the page
which will become highlighted (to indicate the problem areas). After the
feedback is submitted, the server generates an image of the page (with
highlighted elements) and records the url, user agent and time of
submission. Site administrators can then easily view the issues as they
come in. You can view the generated image or the html of the problem
page.

How it works
------------

The web tool allows the user to highlight different elements on the page
(by adding a specific class to those elements). This DOM is then sent to
the server where PhantomJS is used to generate a static image of the
page and the admin interface lets you view the full page contents.

Installation (Standalone)
-------------------------

1. Install the `Django`_ framework
2. Download and extract `PhantomJS`_
3. Checkout this repository.
4. Edit ``settings.py``:

-  Setup your database as necessary
-  Edit the ``PHANTOMJS_EXECUTABLE`` path

5. Initialise the database (don’t forget to setup an administrator)
   ``python manage.py syncdb``
6. Run the server ``python manage.py runserver 8000``

Installation (Shared)
---------------------

Duat can also be installed alongside other django apps.

1. Download and extract `PhantomJS`_
2. Edit ``settings.py``:

-  Add ``PHANTOMJS_EXECUTABLE=<path_to_phantomjs_binary>``
-  Include duat in your ``INSTALLED_APPS`` list

3. Edit your ``urls.py`` and include duat

- ``url(r'^feedback/', include('duat.urls')),``

4. Run syncdb.

Setup
-----

Once you have the server running, you will first need to set up a site
administrator, then create your first project to receive feedback.

1. Visit the admin page (e.g. http://localhost:8000/admin) and log in
   using the admin details you just provided.

First create a project administrator (this is the person who can log
into the back end to view submissions and receive notifications).

2. Click the ‘Add’ button next to the Users section.
3. Enter a username and password and click ‘Save and continue editing’.
4. On the next screen make sure you check the box next to the Staff
   status option.
5. Provide an email address to receive notifications of new feedback
   submissions.
6. In the User Permissions box, select
   ``'duat | feedback | Can change feedback'`` and
   ``'duat | feedback | Readonly Feedback'`` and click the corresponding
   arrow to add these to the box on the right.
7. Save this page.

Now create a Project

8.  Use the ‘Home’ link to go back to the home screen and click ‘Add’
    next to the Projects section.
9.  Provide a name for your project and select the project administrator
    you’ve just created. If you wish to send notifications to this
    administrator click the ‘Notify admin’ checkbox.
10. After clicking the Save button you will have set up your first
    project.

You can then use the javascript link provided on the project screen to
embed a <script> tag onto your site. If duat is being used from within your application, you can reference this script with the following:

    ``<script src="{% url 'duat-feedback' project_name='bos2' %}"></script>``

The project administrator can log into the admin site and will be able
to view the Feedback entries submitted for their corresponding project.

Notes
-----

Inspiration for this system originally came from `feedback.js`_ but I
found the canvas tainting in chrome to be a blocker for our requirements
so I decided to implement a simpler system. 

Tested with Django 1.4, 1.5, 1.6 & 1.7

.. _PhantomJS: http://phantomjs.org/
.. _feedback.js: http://experiments.hertzen.com/jsfeedback/
.. _Google Feedback: http://www.google.com/tools/feedback/intl/en/learnmore.html
.. _Django: https://www.djangoproject.com/

