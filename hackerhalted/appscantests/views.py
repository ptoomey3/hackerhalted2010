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
import hashlib
from django.conf import settings
import os.path
import urllib
from django.db import DatabaseError
import MySQLdb

def session1(request):
    t=loader.get_template('session1_index.html')
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

def session1_authed(request):
    if request.COOKIES.has_key('session_cookie'):
        try:
            session_id = int(request.COOKIES['session_cookie'])
        except ValueError:
            session_id = -1
    else:
        session_id = -1
    try:
        session = Session1.objects.get(session_id=session_id, session_valid=True)
    except Session1.DoesNotExist:
        return HttpResponseRedirect('/appscantests/session1')    
    t=loader.get_template('session1_authed.html')
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

def session1or2(request):
    t=loader.get_template('session1or2_index.html')
    c = Context ({})
    c.update(csrf(request))
      
    return HttpResponse(t.render(c))

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

def session3(request):
    t=loader.get_template('session3_index.html')
    c = Context ({})
    c.update(csrf(request))
      
    return HttpResponse(t.render(c))
    
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

def session4(request):
    t=loader.get_template('session4_index.html')
    c = Context ({})
    c.update(csrf(request))
      
    return HttpResponse(t.render(c))

def session4_login(request):
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")  
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return HttpResponseRedirect('/appscantests/session4')
    
    max_session_id = Session4.objects.all().aggregate(Max('session_id'))['session_id__max']
    if not max_session_id:
        max_session_id = 1
    next_session_id = max_session_id + 1
    session_id_hash = hashlib.md5(str(next_session_id)).hexdigest()
    session = Session4(session_id=next_session_id, session_id_hash=session_id_hash, user=user, session_valid=True)
    session.save()
    response = HttpResponseRedirect('/appscantests/session4_authed')
    response.set_cookie('session_cookie', session_id_hash)
    return response

def session4_authed(request):
    if request.COOKIES.has_key('session_cookie'):
        session_id_hash = request.COOKIES['session_cookie']
    else:
        session_id_hash = ''
    try:
        session = Session4.objects.get(session_id_hash=session_id_hash, session_valid=True)
    except Session4.DoesNotExist:
        return HttpResponseRedirect('/appscantests/session4')
    t=loader.get_template('session4_authed.html')
    c = Context ({})
    return HttpResponse(t.render(c))

def session4_logout(request):
    if request.COOKIES.has_key('session_cookie'):
        session_id_hash = request.COOKIES['session_cookie']
    else:
        session_id_hash = ''
    try:
        session = Session4.objects.get(session_id_hash=session_id_hash)
        session.session_valid = False;
        session.save()
    except Session4.DoesNotExist:
        pass
    response = HttpResponseRedirect('/appscantests/session4')
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

# Landing page
def dirtraverse(request):
    t=loader.get_template('dirtraverse.html')
    c = Context()   
    return HttpResponse(t.render(c))

def openorerror(fname):
    try:
        f = open(fname, 'r')
        return HttpResponse(f)
    except IOError:
        return HttpResponse("Could not open %s" % fname)
    
# Test case: fn=../../../../../../../../../etc/passwd
def dirtraverse1(request):
    data = request.GET.get('fn', '')
    fname = settings.MEDIA_ROOT + data
    return openorerror(fname)

# Test case: fn=....//....//....//....//....//....//....//....//....//....//etc/passwd
def dirtraverse2(request):
    data = request.GET.get('fn', '')
    fname = settings.MEDIA_ROOT + data.replace('../', '')
    return openorerror(fname)

# Test case: dn=../../../../../../../../../etc&fn=passwd
def dirtraverse3(request):
    data = request.GET.get('fn', '')
    data2 = request.GET.get('dn', '')
    fname = settings.MEDIA_ROOT + data2 + "/" + os.path.basename(data)
    return openorerror(fname)

# Test case: fn=../../settings (should be tested test == ./test), showing reliance on /etc/passwd or similar
def dirtraverse4(request):
    data = request.GET.get('fn', '')
    fname = settings.MEDIA_ROOT + data + ".py"
    return openorerror(fname)

# Test case: fn=../../../../../../../../../etc/passwd%00 (emulate null byte truncation)
def dirtraverse5(request):
    data = request.GET.get('fn', '')
    fname = settings.MEDIA_ROOT + data + ".txt"
    fname = fname.partition('\x00')[0]
    return openorerror(fname)

# Test case: fn=.../.../.../.../.../.../.../etc/passwd
def dirtraverse6(request):
    data = request.GET.get('fn', '')
    fname = settings.MEDIA_ROOT + data.replace('..', '.')
    return openorerror(fname)

# Test case: fn=.../.../.../.../.../.../.../etc/passwd%00 (combo)
def dirtraverse7(request):
    data = request.GET.get('fn', '')
    fname = settings.MEDIA_ROOT + data.replace('..', '.') + ".txt"
    fname = fname.partition('\x00')[0]
    return openorerror(fname)

# Test case: fn=..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd (double decode after check)
def dirtraverse8(request):
    data = request.GET.get('fn', '')
    fname = settings.MEDIA_ROOT + os.path.basename(data)
    fname = urllib.unquote(fname)
    return openorerror(fname)

def handle_uploaded_file(f):
    destination = open(settings.SITE_ROOT + '/upload_files/' + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def fileupload(request):
    if len(request.FILES) == 0:
        t=loader.get_template('fileupload_index.html')
        c = Context()   
        return HttpResponse(t.render(c))
    else:
        handle_uploaded_file(request.FILES['upload_file'])
        t=loader.get_template('fileupload.html')
        c = Context({'fname': request.FILES['upload_file'].name})   
        return HttpResponse(t.render(c))

def blind_sql_injection1(request):
    query = request.GET.get('query', '')
    conn = MySQLdb.connect (host = "localhost",
                           user = "root",
                           passwd = "root",
                           db = "hackerhalted")
    cursor = conn.cursor()
    try:
        query = "SELECT data1 FROM appscantests_sqlinjectiondata WHERE data1='" + query + "'"
        cursor.execute(query)
        result = 'Good Query'
    except MySQLdb.ProgrammingError:
        result = 'Bad Query'
    cursor.close()
    conn.close()
    
    return HttpResponse(result)

def blind_sql_injection2(request):
    query = request.GET.get('query', '')
    conn = MySQLdb.connect (host = "localhost",
                           user = "root",
                           passwd = "root",
                           db = "hackerhalted")
    cursor = conn.cursor()
    try:
        query = "SELECT data1 FROM appscantests_sqlinjectiondata WHERE data1='" + query + "'"
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            result = "Results"
        else:
            result = 'No Results'
    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError):
        result = 'No Results'
    cursor.close()
    conn.close()
    
    return HttpResponse(result)

def blind_sql_injection3(request):
    query = request.GET.get('query', '')
    conn = MySQLdb.connect (host = "localhost",
                           user = "root",
                           passwd = "root",
                           db = "hackerhalted")
    cursor = conn.cursor()
    try:
        query = "SELECT data1 FROM appscantests_sqlinjectiondata WHERE data1='" + query + "'"
        cursor.execute(query)
        cursor.execute(query)
        cursor.execute(query)
        result = 'Good Query'
    except MySQLdb.ProgrammingError:
        result = 'Bad Query'
    cursor.close()
    conn.close()
    
    return HttpResponse(result)

def blind_sql_injection4(request):
    query = request.GET.get('query', '')
    conn = MySQLdb.connect (host = "localhost",
                           user = "root",
                           passwd = "root",
                           db = "hackerhalted")
    cursor = conn.cursor()
    try:
        query = "SELECT data1 FROM appscantests_sqlinjectiondata WHERE data1='" + query + "'"
        cursor.execute(query)
        cursor.execute(query)
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            result = "Results"
        else:
            result = 'No Results'
    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError):
        result = 'No Results'
    cursor.close()
    conn.close()
    
    return HttpResponse(result)

def blind_sql_injection5(request):
    query = request.GET.get('query', '')
    conn = MySQLdb.connect (host = "localhost",
                           user = "root",
                           passwd = "root",
                           db = "hackerhalted")
    cursor = conn.cursor()
    try:
        query = "SELECT data1 FROM appscantests_sqlinjectiondata WHERE (data1='" + query + "' and 2=2)"
        cursor.execute(query)
        result = 'Good Query'
    except MySQLdb.ProgrammingError:
        result = 'Bad Query'
    cursor.close()
    conn.close()
    
    return HttpResponse(result)