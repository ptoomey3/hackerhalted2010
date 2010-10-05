# Create your views here.
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, Context, loader
from django.core.context_processors import csrf
from hackerhalted.appscantests.models import *
from django.shortcuts import get_object_or_404
from django.db.models import Max
import random
from django.utils.safestring import mark_safe
from django.core.validators import email_re


def session1(request):
    t=loader.get_template('session1_index.html')
    c = Context ({})
    c.update(csrf(request))
      
    return HttpResponse(t.render(c))

def session1or2(request):
    t=loader.get_template('session1or2_index.html')
    c = Context ({})
    c.update(csrf(request))
      
    return HttpResponse(t.render(c))

def session3(request):
    t=loader.get_template('session3_index.html')
    c = Context ({})
    c.update(csrf(request))
      
    return HttpResponse(t.render(c))
    
def session1_login(request):
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")  
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return HttpResponseRedirect('/appscantests/session1')
    
    max_session_id = Session1.objects.all().aggregate(Max('session_id'))['session_id__max']
    if not max_session_id:
        max_session_id = 100000
    next_session_id = max_session_id + 1
    session = Session1(session_id=next_session_id, user=user, session_valid=True)
    session.save()
    response = HttpResponseRedirect('/appscantests/session1_authed')
    response.set_cookie('session_cookie', next_session_id)
    return response

def session1or2_login(request):
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")  
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return HttpResponseRedirect('/appscantests/session1or2')

    session_table_num = random.randint(1,2)
    if session_table_num == 1:
        session_table = Session1
    else:
        session_table = Session2
    max_session_id = session_table.objects.all().aggregate(Max('session_id'))['session_id__max']
    if not max_session_id:
        max_session_id = 100000 * session_table_num
    next_session_id = max_session_id + 1
    session = session_table(session_id=next_session_id, user=user, session_valid=True)
    session.save()
    response = HttpResponseRedirect('/appscantests/session1or2_authed')
    response.set_cookie('session_cookie', next_session_id)
    return response

def session3_login(request):
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")  
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return HttpResponseRedirect('/appscantests/session3')
    
    try:
        session = Session3.objects.get(session_id=user.username, user=user)
        session.session_valid = True
    except Session3.DoesNotExist:
        session = Session3(session_id=user.username, user=user, session_valid=True)
    session.save()
    response = HttpResponseRedirect('/appscantests/session3_authed')
    response.set_cookie('session_cookie', user.username)
    return response

    
def session1_authed(request):
    if request.COOKIES.has_key('session_cookie'):
        try:
            session_id = int(request.COOKIES['session_cookie'])
        except ValueError:
            session_id = -1
    else:
        session_id = -1
    session = Session1.objects.filter(session_id=session_id, session_valid=True)
    if not session:
        return HttpResponseRedirect('/appscantests/session1')
    else:
        t=loader.get_template('session1_authed.html')
        c = Context ({})
        return HttpResponse(t.render(c))
    
def session1or2_authed(request):
    if request.COOKIES.has_key('session_cookie'):
        try:
            session_id = int(request.COOKIES['session_cookie'])
        except ValueError:
            session_id = -1
    else:
        session_id = -1
    session = Session1.objects.filter(session_id=session_id, session_valid=True) or Session2.objects.filter(session_id=session_id, session_valid=True)
    if not session:
        return HttpResponseRedirect('/appscantests/session1or2')
    else:
        t=loader.get_template('session1or2_authed.html')
        c = Context ({})
        return HttpResponse(t.render(c))
    
def session3_authed(request):
    if request.COOKIES.has_key('session_cookie'):
        try:
            session_id = request.COOKIES['session_cookie']
        except ValueError:
            session_id = ''
    else:
        session_id = ''
    session = Session3.objects.filter(session_id=session_id, session_valid=True)
    if not session:
        return HttpResponseRedirect('/appscantests/session3')
    else:
        t=loader.get_template('session3_authed.html')
        c = Context ({})
        return HttpResponse(t.render(c))

    
def session1_logout(request):
    if request.COOKIES.has_key('session_cookie'):
        try:
            session_id = int(request.COOKIES['session_cookie'])
        except ValueError:
            session_id = -1
    else:
        session_id = -1
    try:
        session = Session1.objects.get(session_id=session_id)
        session.session_valid = False;
        session.save()
    except Session1.DoesNotExist:
        pass
    response = HttpResponseRedirect('/appscantests/session1')
    response.set_cookie('session_cookie', '0')
    return response

def session1or2_logout(request):
    if request.COOKIES.has_key('session_cookie'):
        try:
            session_id = int(request.COOKIES['session_cookie'])
        except ValueError:
            session_id = -1
    else:
        session_id = -1
    try:
        session = Session1.objects.get(session_id=session_id)
        session.session_valid = False;
        session.save()    
    except Session1.DoesNotExist:
        try:
            session = Session2.objects.get(session_id=session_id)
            session.session_valid = False;
            session.save()    
        except Session2.DoesNotExist:
            pass
    response = HttpResponseRedirect('/appscantests/session1or2')
    response.set_cookie('session_cookie', '0')
    return response

def session3_logout(request):
    if request.COOKIES.has_key('session_cookie'):
            session_id = request.COOKIES['session_cookie']
    else:
        session_id = ''
    try:
        session = Session3.objects.get(session_id=session_id)
        session.session_valid = False;
        session.save()    
    except Session3.DoesNotExist:
        pass
    response = HttpResponseRedirect('/appscantests/session3')
    response.set_cookie('session_cookie', '')
    return response


def xss_reflected1(request):
    t=loader.get_template('xss_reflected1.html')
    var1 = request.GET.get('var1', '')
    c = Context({'var1':mark_safe(var1)})
      
    return HttpResponse(t.render(c))

def xss_stored1(request):
    t=loader.get_template('xss_stored1.html')
    data = request.GET.get('data', '')  
    xss_data = XSSData(data=data)
    xss_data.save()
    c = Context({'id':xss_data.id})
    return HttpResponse(t.render(c))

def xss_stored1_get_xssdata(request):
    t=loader.get_template('xss_stored1_get_xssdata.html')
    id = request.GET.get('id', -1)
    try:
        xss_data = XSSData.objects.get(id=id)
        data = xss_data.data
    except XSSData.DoesNotExist:
        data = ''
    c = Context({'data':mark_safe(data)})
    return HttpResponse(t.render(c))

def xss_stored2(request):
    t=loader.get_template('xss_stored2.html')
    data = request.GET.get('data', '')  
    email = request.GET.get('email', '')
    try:
        xss_data = XSSData2.objects.get(email=email)
        xss_data.data = data
    except XSSData2.DoesNotExist:
        xss_data = XSSData2(data=data, email=email)
    xss_data.save()
    c = Context({})
    c.update(csrf(request))
    return HttpResponse(t.render(c))

def xss_stored2_get_xssdata(request):
    t=loader.get_template('xss_stored2_get_xssdata.html')
    email = request.POST.get('email', '')
    try:
        xss_data = XSSData2.objects.get(email=email)
        data = xss_data.data
    except XSSData2.DoesNotExist:
        data = ''
    c = Context({'data':mark_safe(data)})
    return HttpResponse(t.render(c))

def xss_stored3(request):
    t=loader.get_template('xss_stored3.html')
    data = request.GET.get('data', '')  
    xss_data = XSSData(data=data)
    xss_data.save()
    c = Context({'id':xss_data.id})
    c.update(csrf(request))
    return HttpResponse(t.render(c))

def xss_stored3_get_xssdata(request):
    t=loader.get_template('xss_stored3_get_xssdata.html')
    id = request.POST.get('id', -1)
    try:
        xss_data = XSSData.objects.get(id=id)
        data = xss_data.data
    except XSSData.DoesNotExist:
        data = ''
    c = Context({'data':mark_safe(data)})
    return HttpResponse(t.render(c))


def sensitiveinfo1(request):
    t=loader.get_template('sensitiveinfo1.html')
    sensitive_data = SensitiveData.objects.all()
    c = Context({'data':sensitive_data})
    return HttpResponse(t.render(c))

def sensitiveinfo2(request):
    t=loader.get_template('sensitiveinfo2.html')
    sensitive_data = SensitiveData.objects.all()
    c = Context({'data':sensitive_data})
    return HttpResponse(t.render(c))

def sensitiveinfo3(request):
    t=loader.get_template('sensitiveinfo3.html')
    sensitive_data = SensitiveData.objects.all()
    parsed_data = [x.data.split('-') for x in sensitive_data]      
    c = Context({'data':parsed_data})
    return HttpResponse(t.render(c))

def sensitiveinfo4(request):
    t=loader.get_template('sensitiveinfo4.html')
    sensitive_data = SensitiveData.objects.all()
    parsed_data = [x.data.split('-') for x in sensitive_data]      
    c = Context({'data':parsed_data})
    
    return HttpResponse(t.render(c))