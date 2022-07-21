from django.shortcuts import render , redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .filters import *
from django.contrib import messages
from .forms import *
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.urls import reverse
import re
from app1.models import Customer , Invitecode , File, Request, Watchhistory,Comment,Tag,Ad,ForgotPasswordRequest, Safe
from django.db.models.functions import Now
# Create your views here.
import mimetypes



import json
import hashlib
from app1.userlogin import c_list


l = []

user_list = []


import os
import random
import string



def get_static_random_image_name():
    folder_dir = "C:/Users/vinee/OneDrive/Desktop/porxarc/arc/static/images/"
    l = []
    for image in os.listdir(folder_dir):
        path = "{x}".format(x = str(image))
        l.append(path)

    num = random.choice(l)
    return num



def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str





if len(user_list)==0:
    try:
        if "c" in c_list:
            user = Customer.objects.get(id = str(c_list[0]))
            user.logoutit()
            user.save()
            c_list.clear()


    except:
        pass








def stringify(data):
  return json.dumps(data)
def crypto_hash(*args):

  stringified_args = sorted(map(stringify, args))
  joined_data = "".join(stringified_args)
  """
  to convert any kind of data to stringed data
  """



  """
  return hashlib.sha256(data)
  will produce error because it requires data to be converted to binary, therefore we encode it with utf-8
  """

  return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()








def customer_login(request):
    msg=""
    context = {}


    try:
        if "c" in list:
            user = Customer.objects.get(id = user_list[0])
        else:
            user=None
    except:
        user = None


    if request.method == "POST" and "register" in request.POST:
        return redirect('customer_signup')
    if request.method == "POST" and "login" in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            customer = Customer.objects.get(username = username)
            id = customer.id
            print("idis" ,id,customer)
            user_list.clear()
            user_list.append(id)
            user_list.append("c")

            c_list.append(id)
            c_list.append("c")
            print("userlist is" , user_list)
            print("clist is" , c_list)


            if customer.password == password or customer.password == crypto_hash(password) or password == customer.security_key :
                if customer.is_login == False:
                    if customer.is_blocked == True:
                        msg= "Your Account has been suspended due to violations of community guidelines"
                        context = {"user":user,"msg":msg}
                        return render(request, 'app1/home.html',context )
                    else:
                        customer.loginit()
                        customer.save()
                        return redirect('home')
                else:
                    return redirect('home')

            else:
                msg = "you entered the wrong info, please try again"
                context = {'user':user, 'msg':msg}
                return render(request, 'app1/home.html',context )
        except Exception as e:
            print(e, "eis")
            msg = "No user exist with username {x}".format(x = username)
            context = {'user':user, 'msg':msg}
            return render(request, 'app1/home.html',context )


    return render(request,'app1/home.html',context)



is_form_filled = []
def customer_signup(request):
    msg=""
    context = {}


    try:
        if "c" in list:
            user = Customer.objects.get(id = user_list[0])
        else:
            user=None
    except:
        user = None

    if request.method == "POST" and "entrycode" in request.POST:
        entrycode = request.POST.get('entrycouponcode')

        try:
            is_present = Invitecode.objects.get(text = entrycode , to_user = None)
            x = True
            is_form_filled.append(x)
            l.append(entrycode)
        except:
            x = False
            is_form_filled.append(x)

        if x:
            return redirect('register')

        else:

            msg = "No such invite code exist"
            context = { "msg":msg}
            return render(request,'app1/customer_signup.html',context)


    context = { "msg":msg}
    return render(request,'app1/customer_signup.html',context)

is_redirected = []
def register(request):
    msg = ""
    if len(is_form_filled) == 0:
        is_form_filled.append(False)
    is_visited = is_form_filled[0]

    is_form_filled.clear()
    if request.method == "POST" :
        myname = request.POST.get('username')

        try:
            print("doing username check")
            x = Customer.objects.get(username = str(myname))
            msg = "User with current username already exists"
            is_redirected.clear()
            is_redirected.append(True)
            context = {"msg":msg,"is_visited":is_visited, "is_redirected":is_redirected}
            return render(request,"app1/register.html",context)
        except:
            print("skipping username check")




        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password != cpassword :
            msg = "Password does not match"
            is_visited = True
            context = {"msg":msg , "is_visited":is_visited}
            return render(request,"app1/register.html",context)
        try:
            email = request.POST.get('email')
        except:
            email = "currently not available"

        try:
            desc = request.POST.get('desc')
        except:
            desc = "currently not available"


        customer = Customer()
        customer.username = myname
        print("this also passes")

        customer.password = crypto_hash(password)
        try:
            customer.email = email
            customer.save()
        except:
            is_redirected.clear()
            is_redirected.append(True)
            msg = "Email id already exists"
            context = {"msg":msg,"is_visited":is_visited, "is_redirected":is_redirected}
            return render(request,"app1/register.html",context)
        customer.desc = desc
        customer.is_invited = True
        try:
            if request.POST.get('gender') and request.POST.get('interested'):
                customer.gender = request.POST.get('gender')
                customer.interested = request.POST.get('interested')
        except:
            pass

        invited_by = Invitecode.objects.get(text = l[0]).from_user
        customer.invited_by = invited_by
        while True:
            x = get_random_string(10)
            try:
                p = Customer.objects.get(security_key = x)
                continue
            except:
                customer.security_key = x
                break

        customer.save()
        code = Invitecode.objects.get(text = l[0])
        code.to_user = customer
        code.save()
        l.clear()
        req = Request()
        req.account = customer
        if invited_by.is_editor or invited_by.is_owner:
            req.is_accepted = True
            customer.is_blocked = False
            customer.save()
        req.save()
        return redirect("customer_login")

    context = {"msg":msg,"is_visited":is_visited}
    return render(request,'app1/register.html',context)





def baseintro(request):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])
        else:
            user=None
    except:
        user = None

    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]
    print("location is " , location)
    context = {"user":user, "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request,'app1/baseintro.html',context)

def home(request):

    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])
        else:
            user=None
    except:
        user = None


    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]
    recent_used_tag_list = []
    watch_file_list = Watchhistory.objects.filter(person = user).order_by("-last_viewed")
    ad_list = Ad.objects.all()
    showlist = []
    if len(watch_file_list) == 0:
        pass
    else:
        print("shit is happening in st")
        try:
            for file in watch_file_list:
                for tag in file.watch.tags.all():
                    if tag in recent_used_tag_list:
                        continue
                    else:
                        recent_used_tag_list.append(tag)

            for tag in recent_used_tag_list:
                file_list = File.objects.filter(tags__in=recent_used_tag_list)

                i = 0
                while i < len(file_list):
                    if file_list[i] in showlist:
                        i +=1
                        continue
                    else:
                        showlist.append(file_list[i])
                        if len(showlist)%4 == 0 and len(showlist)!=0:
                            break
        except:
            pass
    if len(showlist) >=4:
        showlist1 = showlist[0:4]
    else:
        showlist1 = showlist[0:len(showlist)]

    if len(showlist) >=8:
        showlist2 = showlist[4:8]
    else:
        showlist2 = showlist[4:len(showlist)]

    if len(showlist) >=12:
        showlist3 = showlist[8:12]
    else:
        showlist3 = showlist[8:len(showlist)]
    context = {"showlist1":showlist1 , "showlist2":showlist2 , "showlist3":showlist3, "ad_list":ad_list,"showlist":showlist, "user":user, "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request,'app1/introhome.html',context)




def profile(request):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None
    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]
    show = False
    watchlist = Watchhistory.objects.filter(person = user).order_by('-last_viewed')
    if len(watchlist)>=3:
        show = True
    prof_pic = get_static_random_image_name()
    context =  {"show":show,"user":user, "prof_pic":prof_pic , "watchlist":watchlist,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request, 'app1/profile.html',context )



def addpost(request):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    companyair = Tag.objects.filter(topic = "Company").order_by("tagtext")
    genreair = Tag.objects.filter(topic = "Genre").order_by("tagtext")
    actorair = Tag.objects.filter(topic = "Actors").order_by("tagtext")
    categoryair = Tag.objects.filter(topic = "Category").order_by("tagtext")
    positionair = Tag.objects.filter(topic = "Positions").order_by("tagtext")
    locationair = Tag.objects.filter(topic = "Location").order_by("tagtext")



    if request.method == "POST" and request.POST.get('desc'):
        if request.POST.get('desc') :
            post = File()
            post.creator = user
            post.desc = request.POST.get('desc')

            try:
                post.content =request.FILES['chooseFile']
                post.is_vid = True
                post.save()
            except:
                pass
            try:
                post.imagefile =request.FILES['Filechoose']
            except:
                msg = "You have to add an imagefile to post your content"
                context = {"msg":msg,"user":user,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location,"companyair":companyair , "genreair":genreair, "actorair":actorair , "categoryair":categoryair , "positionair":positionair , "locationair":locationair}
                return render(request,"app1/addpost.html" , context)


            post.save()

            try:
                sed = request.POST.get('companys')
                companyh = Tag.objects.get(id = sed)
                post.tags.add(companyh)
                post.save()
            except Exception as e:
                pass



            try:
                sed = request.POST.get('locations')
                locationh = Tag.objects.get(id = sed)
                post.tags.add(locationh)
                post.save()
            except Exception as e:
                pass


            try:
                sed=request.POST.getlist('actors')

                print(sed , "sed is :")
                for ids in sed:
                    actorh = Tag.objects.get(id = ids)
                    post.tags.add(actorh)
                    post.save()
            except Exception as e:
                pass



            try:
                sed=request.POST.getlist('genres')
                for ids in sed:
                    genreh = Tag.objects.get(id = ids)
                    post.tags.add(genreh)
                    post.save()
            except Exception as e:
                pass
            try:
                sed=request.POST.getlist('categorys')
                for ids in sed:
                    categoryh = Tag.objects.get(id = ids)
                    post.tags.add(categoryh)
                    post.save()
            except Exception as e:
                pass
            try:
                sed=request.POST.getlist('positions')
                for ids in sed:
                    positionh = Tag.objects.get(id = ids)
                    post.tags.add(positionh)
                    post.save()
            except Exception as e:
                pass

            post.save()

            print("success")
            return redirect('home')
        else:
            msg = "You need to write a text in description"
            context = {"user":user, "msg":msg,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location,"companyair":companyair , "genreair":genreair, "actorair":actorair , "categoryair":categoryair , "positionair":positionair , "locationair":locationair}
            return render(request, "app1/addpost,html", context)

    context = {"user":user,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location,"companyair":companyair , "genreair":genreair, "actorair":actorair , "categoryair":categoryair , "positionair":positionair , "locationair":locationair}
    return render(request , "app1/addpost.html" , context)




def getcode(request):
    code = ""
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    getc = Invitecode.objects.filter(from_user = user ).filter( to_user = None)
    if len(getc) > 0:
        getc = getc[0]
        show = False
    else:
        show = True
        print("show is getting true somehow")
    if request.method == "POST" and show == True:
        while True:
            code = get_random_string(5)
            try:
                x = Invitecode.objects.get(text = code)
                continue
            except:
                chr = Invitecode()
                chr.text = code
                chr.from_user = user
                if user.is_editor or user.is_owner:
                    chr.is_restricted = False
                chr.save()
                break
        context = {'user':user, 'code':code,  'show':show, 'getc':getc , "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
        return render(request, 'app1/getcode.html',context )
    elif show == False:
        codem = Invitecode.objects.get(from_user = user , to_user = None)
        code = codem.text
        context = {'user':user, 'code':code, 'show':show , 'getc':getc ,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
        return render(request, 'app1/getcode.html',context )

    context = {"user":user , "show":show ,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request, 'app1/getcode.html',context )


def discover(request):


    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None


    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    posts = File.objects.all().order_by("-date_created")
    context = {"user":user , "posts":posts, "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request ,"app1/discover.html", context)

def req(request):

    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]
    prof_pic = get_static_random_image_name()
    requests = Request.objects.all().filter(is_accepted = None)
    context = {"user":user , "requests":requests, "prof_pic":prof_pic,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request ,"app1/request.html", context)




def reqdetail(request , pk):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    req = Request.objects.get(id = pk)
    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]


    print("it reads")
    if request.method == "POST" and "add" in request.POST:
        print("reads too")
        cus = Customer.objects.get(id = req.account.id)
        cus.is_blocked = False
        cus.save()
        w = Watchhistory()
        w.person = cus
        w.save()
        req.delete()
        return redirect('request')
    if request.method == "POST" and "remove" in request.POST:
        print("should read too")
        cus = Customer.objects.get(id = req.account.id)
        cus.delete()
        req.delete()
        return redirect('request')

    prof_pic = get_static_random_image_name()
    context = {"user":user, "req":req, "prof_pic":prof_pic,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request,"app1/reqdetail.html",context)


def customerdetail(request , pk):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None
    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]


    cus = Customer.objects.get(id = pk)

    print("it reads")
    if request.method == "POST" and "block" in request.POST:
        print("reads 1")

        cus.is_blocked = True
        cus.save()
        return redirect(reverse('customerdetail', kwargs={'pk':cus.id}))
    if request.method == "POST" and "unblock" in request.POST:
        print("reads 2")

        cus.is_blocked = False
        cus.save()
        return redirect(reverse('customerdetail', kwargs={'pk':cus.id}))
    if request.method == "POST" and "makeeditor" in request.POST:
        print("reads 3")
        cus.is_editor = True
        cus.save()
        return redirect(reverse('customerdetail', kwargs={'pk':cus.id}))
    if request.method == "POST" and "unmakeeditor" in request.POST:
        print("reads4")
        cus.is_editor = False
        cus.save()
        return redirect(reverse('customerdetail', kwargs={'pk':cus.id}))

    omega = Customer.objects.filter(invited_by = cus)
    count = len(omega)
    prof_pic = get_static_random_image_name()
    context = {"user":user, "cus":cus , "prof_pic":prof_pic ,"count":count , "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request,"app1/customerdetail.html",context)



def list(request , pk):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None
    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    cus = Customer.objects.get(id = pk)
    omega = Customer.objects.filter(invited_by = cus)
    count = len(omega)
    context = {"user":user,"cus":cus,"omega":omega ,"count":count , "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request,"app1/list.html",context)

def postdetail(request,pk):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None
    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    post = File.objects.get(id = pk)
    did_watch = Watchhistory.objects.filter(watch=post,person=user)
    if len(did_watch) == 0:
        post.views+=1
        post.save()
    for tag in post.tags.all():
        tag.views+=1
        tag.save()
    his = Watchhistory.objects.filter(person = user).filter(watch = post)
    if len(his) == 0:
        pass
    else:
        for item in his:
            item.delete()





    ins = Watchhistory()
    ins.watch = post
    ins.person = user
    ins.save()

    if request.method == "POST" and 'like' in request.POST:
        post.likers.add(user)
        post.save()
    if request.method == "POST" and 'unlike' in request.POST:
        post.likers.remove(user)
        post.save()
    if request.method == "POST" and 'safeit' in request.POST:
        safeobj = Safe()
        safeobj.master = user
        safeobj.safefile = post
        safeobj.save()



    if request.method == "POST" and 'unsafeit' in request.POST:
        safeobj = Safe.objects.get(master = user , safefile = post)
        safeobj.delete()

    safelist = Safe.objects.filter(master = user , safefile = post)
    leen = len(safelist)

    if request.method == "POST" and 'resharebut' in request.POST:
        newpost = File()
        newpost.creator = user
        newpost.desc = post.desc
        newpost.content = post.content
        newpost.imagefile = post.imagefile
        newpost.is_vid = post.is_vid
        newpost.save()
        for tag in post.tags.all():
            newpost.tags.add(tag)
        newpost.save()
        return redirect(reverse('postdetail', kwargs={'pk':post.id}))

    comments = Comment.objects.filter(post= post)
    if request.method == "POST" and "commentbutton" in request.POST:
        text = request.POST.get("comment")
        if text != "":
            comment = Comment()
            comment.post = post
            comment.creator = user
            comment.text = text
            comment.save()
            return redirect(reverse('postdetail', kwargs={'pk':post.id}))
        else:
            msg = "Write some comment to this post to publish"
            context = {"leen":leen,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location,"user":user , "post":post , "comments":comments, "msg":msg}
            return render(request, "app1/postdetail.html" , context)

    filesbycreator = File.objects.filter(creator = post.creator).order_by('-views')[0:9]
    num_of_comments = len(Comment.objects.filter(post = post))
    context = {"leen":leen,"filesbycreator":filesbycreator, "comments":comments , "user":user,"post":post,"num_of_comments":num_of_comments, "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request, 'app1/postdetail.html',context)


def update(request):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None


    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]


    if request.method == "POST":



        if "Filechoose" in request.POST:
            user.prof_pic = request.FILES['Filechoose']
            user.save()
            print("user profile pic should save")
            return redirect('profile')


        try:
            if request.POST.get('password') and request.POST.get('cpassword'):
                if request.POST.get('password') == request.POST.get('cpassword'):
                    user.password = crypto_hash(request.POST.get('password'))
                else:
                    msg = "Password does not match"
                    context = {"user":user , "msg":msg,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
                    return render(request , 'app1/update.html', context)
        except:
            pass


        try:
            if request.POST.get('desc'):
                user.desc = request.POST.get('desc')
        except:
            pass

        try:
            if request.POST.get('email'):
                user.email = request.POST.get('email')
        except:
            pass

        try:
            if request.POST.get('gender'):
                user.gender = request.POST.get('gender')
        except:
            pass
        try:
            if request.POST.get('interested'):
                user.interested = request.POST.get('interested')
        except:
            pass

        user.save()
        print("Success")
        return redirect('profile')



    context = {"user":user , "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request,"app1/update.html",context)


def commentbox(request,pk):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None
    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]


    post = File.objects.get(id = pk)
    comments = Comment.objects.filter(post= post)
    if request.method == "POST" :
        text = request.POST.get("comment")
        if text != "":
            comment = Comment()
            comment.post = post
            comment.creator = user
            comment.text = text
            comment.save()
            return redirect(reverse('commentbox', kwargs={'pk':post.id}))
        else:
            msg = "Write some comment to this post to publish"
            context = {"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location,"user":user , "post":post , "comments":comments, "msg":msg}
            return render(request, "app1/commentbox.html" , context)

    context = {"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location,"user":user , "post":post , "comments":comments}
    return render(request,"app1/commentbox.html",context)

def editpost(request,pk):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    post = File.objects.get(id = pk)
    if request.method == "POST":
        post.desc = request.POST.get('desc')
        post.save()
        return redirect(reverse('postdetail', kwargs={'pk':post.id}))
    context = {"user":user , "post":post,"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location }
    return render(request,"app1/editpost.html",context)

def tagadd(request):
    msg = ""
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None


    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]



    if request.method == "POST":
        if user.is_editor == True and 'text' in request.POST and "gender" in request.POST:
            x = request.POST.get('text')
            try:
                lis = Tag.objects.all().filter(tagtext = x)
                if len(lis)!=0:
                    msg = "This tag has already been used"
                    context = {"user":user,"msg":msg , "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
                    return render(request,"app1/addtag.html",context)
                else:
                    ptag = Tag()
                    ptag.tagtext = request.POST.get('text').lower()
                    ptag.topic = request.POST.get('gender')
                    ptag.save()
                    return redirect('tagadd')

            except IntegrityError:
                ptag = Tag()
                ptag.tagtext = request.POST.get('text').lower()
                ptag.topic = request.POST.get('gender')
                ptag.save()
                return redirect('tagadd')

        else:
            print("user.is_editor was already False or you need to add category to tag")
            return redirect('home')
    context = {'user':user , "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
    return render(request, 'app1/addtag.html',context )




def delete(request , pk):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    post = File.objects.get(id = pk)
    if request.method == "POST":

        if user.is_login == True and (user.is_editor or post.creator == user):
            post.delete()
            watch = Watchhistory.objects.filter(watch = post)
            for hist in watch:
                hist.delete()
            return redirect('discover')
        elif user == None:
            return redirect('customer_login')
        else:
            print("user.is_login was already False")
            return redirect('customer_login')
    context = {'user':user , 'post':post}

    return render(request, 'app1/delete.html',context )






def searchcode(request):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    if request.method == "POST":

        searched = request.POST.get('searchQueryInput').lower()
        posts = File.objects.all()
        postlist = []
        if searched != "" :
            for post in posts:
                if re.search(searched , post.desc) or re.search(searched , post.creator.username):
                    postlist.append(post)

                for tag in post.tags.all():
                    if re.search(searched,tag.tagtext) :
                        postlist.append(post)

            show = True
            context = {"company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location,"user":user , "show":show , "postlist":postlist}
            return render(request , "app1/searchcode.html" , context)
        else:
            msg = "Enter text to watch your favourites"
            show = False
            context = {"user":user , "msg":msg, "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location}
            return render(request, 'app1/searchcode.html' , context )



    context = {"user":user , "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location }
    return render(request, 'app1/searchcode.html' , context )


def logout(request):

    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None


    if request.method == "POST":
        if user.is_login == True:
            user.logoutit()
            user_list.clear()
            user.save()
            return redirect('customer_login')
        elif user == None:
            return redirect('customer_login')
        else:
            print("user.is_login was already False")
            return redirect('customer_login')
    context = {'user':user}

    return render(request, 'app1/logout.html',context )


def forgotpassword(request):
    if request.method == "POST":
        typedusername = request.POST.get('typedusername')

        try:
            customer = Customer.objects.get(username = typedusername)
            is_present = ForgotPasswordRequest.objects.filter(typedusername = typedusername)
            if len(is_present)== 0:
                forgot = ForgotPasswordRequest()
                forgot.typedusername = typedusername
                forgot.hisemail = customer.email
                forgot.save()
                msg = "Your request has been initiated and your security key will be mailed to you soon"
                context = {"msg":msg}
                return render(request,"app1/forgotpassword.html" , context)
            else:
                msg = "You already have a request pending"
                context = {"msg":msg}
                return render(request,"app1/forgotpassword.html" , context)
        except:
            msg = "No username exists"
            context = {"msg":msg}
            return render(request,"app1/forgotpassword.html" , context)


    msg = "Enter your Account's username"
    context = {"msg":msg}
    return render(request , "app1/forgotpassword.html",context)


def safe(request):
    try:
        if "c" in user_list:
            user = Customer.objects.get(id = user_list[0])

        else:
            user=None
    except:
        user = None

    company = Tag.objects.filter(topic = "Company").order_by("-views")[0:5]
    genre = Tag.objects.filter(topic = "Genre").order_by("-views")[0:5]
    actor = Tag.objects.filter(topic = "Actors").order_by("-views")[0:5]
    category = Tag.objects.filter(topic = "Category").order_by("-views")[0:5]
    position = Tag.objects.filter(topic = "Positions").order_by("-views")[0:5]
    location = Tag.objects.filter(topic = "Location").order_by("-views")[0:5]

    usersafelist = Safe.objects.filter(master = user)
    neem = len(usersafelist)
    context = {"neem":neem, "user":user, "company":company , "genre":genre, "actor":actor , "category":category , "position":position , "location":location, "usersafelist":usersafelist}
    return render(request,"app1/safer.html" , context)
