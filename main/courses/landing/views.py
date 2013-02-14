from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from c2g.models import Course
from django.db.models import Q

def landing(request):
    """For normal servers, return our project landing page.  For maint servers,
    show our maintenance page.  Hiring shows a little banner stripe."""
    hiring=True
    context = RequestContext(request)

    """ if logged in show institution courses if appropriate 
        other rules: superuser - sees all
                     staff - sees all from institution?
    """
    
    if not request.user.is_authenticated():
        course_list = {}
    else:
        group_list = request.user.groups.all()
        course_list = Course.objects.filter(Q(student_group_id__in=group_list, mode='ready') | Q(instructor_group_id__in=group_list, mode='ready') | Q(tas_group_id__in=group_list, mode='ready') | Q(readonly_tas_group_id__in=group_list, mode='ready'))
    site = getattr(settings, 'SITE_NAME_SHORT')
    r = render_to_response("sites/%s/landing.html" % site,
            {'hiring': hiring, 
             'course_list':course_list,
             'display_login': request.GET.__contains__('login')},
             context_instance=context)
    return r
    

def hiring(request):
    context = RequestContext(request)
    site = getattr(settings, 'SITE_NAME_SHORT')
    return render_to_response("sites/%s/hiring.html" % site, context_instance=context)
