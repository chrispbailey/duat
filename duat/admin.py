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
    
    readonly_fields = ('created_date','screenshot','page','referrer','user_agent')
    admin_readonly_fields = ('created_date','project','screenshot','page','referrer','user_agent')
    list_display = ('id_render', 'project', 'comment', 'created_date', 'screenshot')
    list_filter = ('project','created_date') # filters for superuser
    admin_list_filter = ('created_date',) # filters visible to project admin only
    search_fields = ['comment']
    list_per_page = 5
    form = FeedbackModelForm
    
    def id_render(self, obj):
        """
        Increase reability of id column
        """
        url = reverse('admin:%s_%s_change' %(obj._meta.app_label,  obj._meta.module_name),  args=[obj.id] )
        return ('<a href="%s">Feedback #%s</a>' % (url, obj.id))
    id_render.allow_tags = True
   
    def screenshot(self, obj):
        """
        Renders a clickable screenshot with links to the full image or html view
        """
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
        """
        Disable add permission from admin interface
        """
        return False

    def get_readonly_fields(self, request, obj=None):
        """
        Only allow superuser to edit fields
        """
        if not request.user.is_superuser and request.user.has_perm('duat.readonly_feedback'):
            list = [f.name for f in self.model._meta.fields]
            list.append('screenshot')
            return list
        return self.readonly_fields

    def queryset(self, request):
        """
        Limit Feedback to those that belong to the project the request's user is admin of.
        """
        qs = super(FeedbackAdmin, self).queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done.
        return qs.filter(project__admin=request.user)
    
    _superuser_filter = list_filter # copy list filter
    def changelist_view(self, request, extra_context=None):
        """
        Change filter options based on user type
        """
        if request.user.is_superuser:
            self.list_filter = self._superuser_filter
        else:
            self.list_filter = self.admin_list_filter
        return super(FeedbackAdmin, self).changelist_view(request, extra_context)
    
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','admin','jslink')
    readonly_fields = ('jslink',)
    
    def project_name(self, project):
        return project.name
    
    def jslink(self, project):
        """
        Provide a link to the embeddable javascript file
        """
        url = reverse('js',kwargs={'project_name':project.name})
        return '<a href="%s">%s</a>' % (url,url)
    jslink.allow_tags = True
    jslink.short_description = 'Javascript link'
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback, FeedbackAdmin)
