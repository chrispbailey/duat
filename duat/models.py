import os

from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

try:
    # Django 1.5
    from django.utils.text import slugify
except:
    # Older versions
    from django.template.defaultfilters import slugify


class Project(models.Model):
    name = models.CharField(max_length=200,
                            unique=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    image = models.ImageField(upload_to='duat_feedback', null=True)
    created_date = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return u'Feedback #%s (%s)' % (self.id, self.project.name)
    
    class Meta:
        ordering = ('-created_date',)
        permissions = (
            ('readonly_feedback','Readonly Feedback'),
        )

@receiver(pre_delete, sender=Feedback)
def _feedback_delete(sender, instance, **kwargs):
    """ Delete auto-generated screenshot when model instance is deleted """
    try:
        os.remove(instance.image.path)
    except OSError:
        pass
