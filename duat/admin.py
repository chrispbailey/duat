from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings

from duat.models import Feedback, Project


class FeedbackModelForm( forms.ModelForm ):
    comment = forms.CharField( widget=forms.Textarea )
    
    class Meta:
        model = Feedback
        fields = "__all__" 


class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['project','comment','screenshot']}),
        ('Details', {'fields': ['page','referrer','user_agent','created_date']}),
    ]

    readonly_fields = ('created_date','screenshot','page','referrer','user_agent')
    admin_readonly_fields = ('created_date','project','screenshot','page','referrer','user_agent')
    list_display = ('id_render', 'project', 'comment', 'created_date', 'screenshot')
    _superuser_filter = ('project','created_date') # filters for superuser
    _admin_list_filter = ('created_date',) # filters visible to project admin only
    list_filter = _superuser_filter
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
        page_url = reverse('duat-view',kwargs={'project_name':obj.project.name,'id':obj.id})

        PHANTOMJS_EXECUTABLE = getattr(settings, 'PHANTOMJS_EXECUTABLE', '')
        if PHANTOMJS_EXECUTABLE and obj.image:
            url_image = obj.image.url
            return ('<a href="%s" style="height:200px;width:200px;'
                    'background-image:url(%s);'
                    'background-repeat:no-repeat;'
                    'display:block;'
                    'background-size: 200px auto;">&nbsp;</a>'
                    'View: <a href="%s">Image</a> | <a href="%s">Page</a>' % 
                    (url_image, url_image, url_image, page_url))
        else:
            # No PhantomJS setup
            return ('View: <a href="%s">Page</a>' %  (page_url))
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


    def changelist_view(self, request, extra_context=None):
        """
        Change filter options based on user type
        """
        if request.user.is_superuser:
            self.list_filter = self._superuser_filter
        else:
            self.list_filter = self._admin_list_filter
        return super(FeedbackAdmin, self).changelist_view(request, extra_context)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','admin')
    readonly_fields = ('jslink',)

    host = None

    def project_name(self, project):
        return project.name

    def jslink(self, project):
        """
        Provide a link to the embeddable javascript file
        """
        url = reverse('duat-feedback',kwargs={'project_name':project.name})
        return '<script src="%s%s"></script>' % (ProjectAdmin.host, url)
    jslink.short_description = 'Embed link'

    def get_readonly_fields(self, request, obj=None):
        if not ProjectAdmin.host:
            # set the class-level host here was we have a request object
            if request.is_secure():
                ProjectAdmin.host = 'https://' + request.get_host()
            else:
                ProjectAdmin.host = 'http://' + request.get_host()
        if obj: # Editing
            return self.readonly_fields
        return ()

admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback, FeedbackAdmin)
