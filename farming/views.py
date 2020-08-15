import runpy
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , get_user_model
from .models import *
from django.db.models import Q
from django.contrib.messages import warning
from django.shortcuts import get_object_or_404
from .forms import RegistrationFormUser , image_data
import uuid,os,shutil
from PIL import Image
from farming import sn
from django.contrib.auth import logout




def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request,'home.html',{})




def home(request):
    return render(request,'home.html',{})


def display_info(request):

    user_info=Person.objects.filter(user=request.user)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$88",user_info)
    return render(request, 'display_info.html', {'details':user_info,'name':user_info.values()[0]['name']})
    

def login1(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
               login(request, user)
               user_info=Person.objects.filter(user=request.user)
               print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$7777",user_info.name)

               return render(request, 'display_info.html', {'details':user_info,'name':user_info.name})
            else:
                return render(request, 'home.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'home.html', {'error_message': 'Invalid login'})
    return render(request,'home.html',{})





def check_new(request):
    return render(request,'add_image.html',{})

def check_new2(request):
    form=image_data
    dis="HEALTHY!!"
    tret="HEALTHY!!"
    acc=""
    acc=0

    mail=Person.objects.filter(user=request.user).values()[0]['email']
    if request.method == 'POST':
        form = image_data(request.POST, request.FILES)
        
        
        if form.is_valid():
            img = Image.open(form.cleaned_data['photo'])
            print(img)
            img.save("detect/pic.jpg")
            #exec(open("mach/sn.py").read())
            #file_globals = runpy.run_path("mach/sn.py")
            #execfile("mach/sn.py")
            dis,tret,acc=sn.openphoto()

            f=open("num.txt","r")
            if f is not None:
                print("opened successfully")
            
            idd=f.read()
            print("&&&&&&&&&&&&&&&8",idd)
            f.close()
            f=open("num.txt","w")
            f.write(str(int(idd)+1))
            f.close()

            a=photo_data(id=idd ,email1=mail,disease=dis,suggestion=tret,photo=form.cleaned_data['photo'] )
            print("TTTTTTTTTTTTTTTTTTTTT",form.cleaned_data['photo'])
            a.save()
            #form.save()
            return render(request,'result.html',{'a':a,'acc':acc})
    else:
        form = image_data()
    return render(request, 'add_image.html', {
        'form': form
    })











"""
    form=image_data
    #print(request.Method)
    if request.method=="POST":
        form=image_data(request.POST)
        if form.is_valid():
            user=request.user
            photo=request.FILES.get('myfile')
            person=Person.objects.filter(user=user)
            email1=person.values()[0]['email']
            disease="LIGHTBLIGHT"
            suggestion="TREATITNOW"
            a=photo_data.objects.create(email1=email1,disease=disease,suggestion=suggestion,photo=photo)
            return render(request,'result.html',{'photo_data':a})
    return render(request,'empty.html',{})"""






def check_old(request):
    person2=Person.objects.filter(user=request.user)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&7",person2.values()[0]['email'])
    image_data=photo_data.objects.filter(email1=person2.values()[0]['email'])
    if image_data :
        print("HEYYYYYYYYYYYY")
        return render(request,'display_photo.html',{'data':image_data})
    return render(request,'empty.html',{})

def delete_pics(request):
    person2=Person.objects.filter(user=request.user)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&7",person2.values()[0]['email'])
    image_data=photo_data.objects.filter(email1=person2.values()[0]['email'])
    image_data.delete()
    return render(request, 'display_info.html', {'details':person2,'name':person2.values()[0]['name']})

def register(request):
    title="Adds Users"
    form = RegistrationFormUser
    print("@@@@@@@@@@@@@@@@",request.method)
    if request.method=="POST":
        form=RegistrationFormUser(request.POST)
        if form.is_valid():

            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            address=form.cleaned_data['address']
            age=form.cleaned_data['age']
            gender=form.cleaned_data['gender']
            profession=form.cleaned_data['profession']

            user=get_user_model().objects.create_user(form.cleaned_data['email'],form.cleaned_data['email'],form.cleaned_data['password'])
            user.save()
            Person.objects.create(user=user,name=name,email=email,address=address,age=age,gender=gender,profession=profession)

            message = "New USER is added"
            return render(request, 'stuff_added.html', {'display_text': message})

    return render(request, 'register.html', {'form': form, 'title': title})


