import os
import re
import tempfile
import json
import logging

from subprocess import call

from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.encoding import smart_str
from django.core.mail import send_mail

from duat.models import Feedback, Project

logger = logging.getLogger(__name__)


def post(request, project_name):
    """
    Store a posted feedback submission
    """
    project = Project.objects.get(name=project_name)

    comment = page = referrer = None
    data = request.POST.get('duat-data',None)

    if data:
        j = json.loads(data.encode("utf-8"))
        html = j['html']
        comment = j['comment']
        referrer = j['referrer']
        page = j['url']

        # process html contents...

        # remove all scripts
        # NB - We are not attempting to comprehensively block XSS, 
        # rather simply disable any javascript from loading
        p = re.compile('<script(.*?)<\/script>', flags=(re.IGNORECASE | re.DOTALL))
        html = p.sub('',html)

        pos = html.find('<head')
        pos = html.find('>',pos)+1

        # insert base tag
        if '<base' not in html and page:
            host = page[:page.find('/',10)]
            html = html[0:pos] + "<base href='"+host+"'></base>" + html[pos:]

    if comment and html:
        feedback = Feedback(project = project,
                            comment = comment,
                            html = html,
                            user_agent = request.META.get('HTTP_USER_AGENT',''),
                            referrer = referrer,
                            page = page)
        feedback.save()
        
        # Create the destination for our screenshot
        feedback.image = "duat_feedback/%s/%s.jpg" % (project, feedback.id)
        feedback.save()

        logger.info('Saved issue %s' % feedback.id)

        generate_screenshot(feedback)

        if project.notify_admin and project.admin.email:
            try:
                url = reverse('admin:%s_%s_change' % (feedback._meta.app_label,
                                                      feedback._meta.module_name),
                              args=[feedback.id])
                url = 'http%s://%s%s' % (('s' if request.is_secure() else ''),
                                         request.META.get('HTTP_HOST'),
                                         url)
                send_mail('DUAT: feedback received',
                          'You can view this item here:\n%s' % url, 
                          settings.DEFAULT_FROM_EMAIL, 
                          [project.admin.email],
                          fail_silently=False)
            except Exception as e:
                logger.warn("Unable to notify admin: %s" % e)

        return HttpResponse("Thanks")
    else:
        logger.error('Not saved - missing data')
        return HttpResponseServerError('Something went wrong')


def view(request, project_name, id):
    project = Project.objects.get(name=project_name)
    feedback = Feedback.objects.get(pk=id, project=project)

    html = feedback.html
    pos = html.find('<head')
    pos = html.find('>',pos)+1

    # add our own admin script
    url = request.META.get('HTTP_HOST') + reverse('duat-admin')
    html = html[0:pos] + "<script src='//%s'></script>" % url + html[pos:]

    return HttpResponse(html)


def generate_screenshot(feedback):
    """ Pass the html onto PhantomJS to convert into an image """
    PHANTOMJS_EXECUTABLE = getattr(settings, 'PHANTOMJS_EXECUTABLE', '')

    if not PHANTOMJS_EXECUTABLE:
        logger.warn('PHANTOMJS_EXECUTABLE not set - skipping screenshot generation')
        return

    output_file = feedback.image.path
    logger.debug("Uploading screenshot to %s" % output_file)

    # create a temp file to write our HTML to
    input_file = tempfile.NamedTemporaryFile(delete=True)

    input_file.write(smart_str(feedback.html))
    # insert base so that static resources are loaded correctly

    # construct parameters to our phantom instance
    args = [PHANTOMJS_EXECUTABLE,
            os.path.dirname(__file__)+"/renderhtml.js",
            input_file.name,
            output_file]

    # create the process
    p = call(args)


def generate_js(request, filename, project_name=None):
    """ 
    Returns a javascript file generated using django's templating mechanism
    """
    project = path = None
    if project_name:
        project = Project.objects.get(name=project_name)
        path = reverse('duat-post', kwargs={'project_name':project.name})
    context = RequestContext(request)
    host = request.META.get('HTTP_HOST')
    context['project'] = project
    context['host'] = host
    context['submit_url'] = path
    context['csrf_token_name'] =settings.CSRF_COOKIE_NAME
    return HttpResponse(render_to_response(filename, context_instance=context),
                        content_type = 'application/javascript')
