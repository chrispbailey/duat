import os

from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

try:
    # Django 1.5
    from django.utils.text import slugify
except:
    # Older versions
    from django.template.defaultfilters import slugify


class Project(models.Model):
    name = models.CharField(max_length=200,
                            unique=True)
    admin = models.ForeignKey(User)
    notify_admin = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        super(Project, self).save(*args, **kwargs) # Call the "real" save() method.
        
    def __unicode__(self):
        return u'%s' % (self.name)


class Feedback(models.Model):
    project = models.ForeignKey(Project)
    page = models.CharField(max_length=2000)
    referrer = models.CharField(max_length=2000)
    user_agent = models.CharField(max_length=2000)
    comment = models.CharField(max_length=2000, null=True)
    html = models.TextField(null=True)
    image = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return u'Feedback #%s (%s)' % (self.id, self.project.name)
    
    class Meta:
        ordering = ('-created_date',)


@receiver(pre_delete, sender=Feedback)
def _feedback_delete(sender, instance, **kwargs):
    """ Delete auto-generated screenshot when model instance is deleted """
    screenshot = "%s/%s.jpg" % (os.path.join(settings.STATIC_ROOT, 'screenshots'),
                                 instance.id)
    try:
        os.remove(screenshot)
    except OSError:
        pass
