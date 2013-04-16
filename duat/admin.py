from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings

from duat.models import Feedback, Project

class FeedbackModelForm( forms.ModelForm ):
    comment = forms.CharField( widget=forms.Textarea )
    
    class Meta:
        model = Feedback

class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['project','comment','screenshot']}),
        ('Details', {'fields': ['page','referrer','user_agent','created_date']}),
    ]
    
    readonly_fields = ('created_date','screenshot','comment','project','page','referrer','user_agent')
    list_display = ('id_render', 'project', 'comment', 'created_date', 'screenshot')
    list_filter = ('project','created_date')
    search_fields = ['comment']
    list_per_page = 5
    form = FeedbackModelForm
    
    def id_render(self, obj):
        url = reverse('admin:%s_%s_change' %(obj._meta.app_label,  obj._meta.module_name),  args=[obj.id] )
        return ('<a href="%s">Feedback #%s</a>' % (url, obj.id))
    id_render.allow_tags = True
   
    def screenshot(self, obj):
        url_image = settings.STATIC_URL + 'screenshots/' + str(obj.id) + '.jpg'
        url_rendered = reverse('view',kwargs={'project_name':obj.project.name,'id':obj.id})
        return ('<a href="%s" style="height:200px;width:200px;'
                'background-image:url(%s);'
                'background-repeat:no-repeat;'
                'display:block;'
                'background-size: 200px auto;">&nbsp;</a>'
                'View: <a href="%s">Image</a> | <a href="%s">Page</a>' % 
                (url_image, url_image, url_image, url_rendered))
    screenshot.allow_tags = True

    def has_add_permission(self, request):
        return False


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','admin','jslink')
    readonly_fields = ('jslink',)
    
    def project_name(self, project):
        return project.name
    
    def jslink(self, project):
        url = reverse('js',kwargs={'project_name':project.name})
        return '<a href="%s">%s</a>' % (url,url)
    jslink.allow_tags = True
    jslink.short_description = 'Javascript link'
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback, FeedbackAdmin)

