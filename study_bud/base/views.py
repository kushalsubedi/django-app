
from distutils.log import error
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import RoomForm
from .models import Message, Room,Topic

# Create your views here.


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not Exixt')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
             message=error(request,'Username or password does not exist ')


   
    context ={}
    return render (request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home (request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    #Implementing The Dynamic Searching Functionality
    rooms=Room.objects.filter(
        Q(topic__name__contains=q) |
        Q (name__icontains=q)|
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body = request.POST.get('body')
        )
        return redirect ('room', pk=room.id)
    context = {'room':room,'room_messages':room_messages}
 
    return render(request,'base/room.html',context)


@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom (request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
 
    context = {'form':form} 
    
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        print("Deletion succesful")
  


    context={'obj':room}
    return render(request,'base/delete.html',context)


