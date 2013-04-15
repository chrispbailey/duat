import os
import re
import tempfile
import urllib2
import base64
import urlparse;
import json
import logging

from subprocess import call

from django.http import HttpResponse
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
	data = request.POST.get('data',None)

	if data:
		j = json.loads(data.encode("utf-8"))
		html = j['html']
		comment = j['comment']
		referrer = j['referrer']
		page = j['url']
		
		# process html contents...
		
		# remove all scripts
		html = re.sub('<script(.*?)<\/script>','',html, 
					  flags=(re.IGNORECASE | re.DOTALL))
		
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
	
		logger.info('Saved issue %s' % feedback.id)
		
		generate_screenshot(feedback)
		
		if project.admin_email:
			url = reverse('admin:%s_%s_change' %(feedback._meta.app_label,  feedback._meta.module_name),  args=[feedback.id] )
			send_mail('Feedback recieved',
					  'You can view this item here\n', 
					  'webmaster@duat', [project.admin_email], fail_silently=False)

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
	url = request.META.get('HTTP_HOST') + reverse('admin')
	html = html[0:pos] + "<script src='//%s'></script>" % url + html[pos:]

	return HttpResponse(html)
	
def generate_screenshot(feedback):
	PHANTOMJS_EXECUTABLE = getattr(settings, 'PHANTOMJS_EXECUTABLE', 'phantomjs')
	output_dir = os.path.join(settings.STATIC_ROOT, 'screenshots')
	output_file = "%s/%s.jpg" % (output_dir, feedback.id) 

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
	
def generate_js(request, project_name, filename):
	project = Project.objects.get(name=project_name)
	context = RequestContext(request)
	path = reverse('post', kwargs={'project_name':project.name})
	return HttpResponse(render_to_response(filename,
										   {'project':project,
											'host' : request.META.get('HTTP_HOST'),
											'path': path},
										   context_instance=context),
						mimetype = 'application/javascript')

def processed_js(request, filename):
	context = RequestContext(request)
	return HttpResponse(render_to_response(filename,
										   {'host' : request.META.get('HTTP_HOST')},
										   context_instance=context),
						mimetype = 'application/javascript')
