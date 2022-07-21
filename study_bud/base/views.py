from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm
from .models import Room
# Create your views here.

def home (request):
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
 
    return render
    
def CreateRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)


def updateRoom (request,pk):
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
 
    context = {'form':form} 
    
    return render(request,'base/room_form.html',context)


def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method== 'POST':
        room.delete()
        print("Deletion succesful")
  


    context={'obj':room}
    return render(request,'base/delete.html',context)