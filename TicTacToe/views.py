from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
import json

from .models import Room


def index(request):
    return render(request, 'TicTacToe/index.html', {})


def rules(request):
    return render(request, 'TicTacToe/rules.html', {})


def LogIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # return render(request, 'TicTacToe/index.html', {})
            return redirect('home')
        else:
            messages.info(request, "The username and password didn't match. Please try again.")
            return render(request, 'TicTacToe/login.html', {})

    return render(request, 'TicTacToe/login.html', {})


def LogOut(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already in use.')
            return render(request, 'TicTacToe/signup.html', {})

        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)

        user.save()

        return redirect('log_in')

    return render(request, 'TicTacToe/signup.html', {})


@login_required(login_url='/log-in')
def myProfile(request):
    if request.method == 'GET' and request.user.is_authenticated:
        fn = request.user.first_name
        ln = request.user.last_name
        em = request.user.email
        un = request.user.username

        return render(request, 'TicTacToe/myProfile.html',
                      {'username': un, 'fn': fn, 'ln': ln, 'email': em})

    return render(request, 'TicTacToe/myProfile.html', {'username': request.user.username})


@login_required(login_url='/log-in')
def myMatches(request):
    myRooms = None
    try:
        myRooms = Room.objects.filter(Q(player1=request.user) | Q(player2=request.user))
        return render(request, 'TicTacToe/myMatches.html', {'myRooms': myRooms})
    except:
        pass

    return render(request, 'TicTacToe/myMatches.html', {'myRooms': myRooms})


@login_required(login_url='/log-in')
def play(request):
    if (request.method == 'POST'):
        RoomName = request.POST.get('RoomName')
        return render(request, 'TicTacToe/play.html', {
            'room_name': RoomName
        })
    return render(request, 'TicTacToe/play.html', {})


@login_required(login_url='/log-in')
def room(request, room_name):
    RoomName = room_name

    # room will always exist if user has come here
    ROOM = Room.objects.get(room_name=RoomName)
    player1Name = ROOM.player1
    player2Name = ROOM.player2
    scoreP1 = ROOM.score_player1
    scoreP2 = ROOM.score_player2

    if (ROOM.player2 == None and ROOM.player1 != request.user):
        room = Room.objects.get(room_name=RoomName)
        room.player2 = request.user
        room.save()
    else:
        if (ROOM.player2 == request.user or ROOM.player1 == request.user):
            pass
        else:
            return redirect('play')

    return render(request, 'TicTacToe/room.html', {
        'room_name': room_name,
        'player1Name': player1Name,
        'player2Name': player2Name,
        'scoreP1': scoreP1,
        'scoreP2': scoreP2,
    })


@login_required(login_url='/log-in')
def validate_room_name(request, room_name):
    RoomName = room_name
    ROOM = None
    try:
        ROOM = Room.objects.get(room_name=RoomName)
    except:
        pass

    data = {
        'is_taken': Room.objects.filter(room_name=RoomName).exists(),
        'is_full': False
    }
    if (data['is_taken'] == False):
        player1 = request.user
        status = '1'
        room = Room(room_name=RoomName, player1=player1, status=status)
        room.save()

    if (data['is_taken'] == True):
        if (ROOM.player2 == None and ROOM.player1 != request.user):
            room = Room.objects.get(room_name=RoomName)
            room.player2 = request.user
            room.save()
        else:
            if (ROOM.player2 == request.user or ROOM.player1 == request.user):
                pass
            else:
                data['is_full'] = True

    return JsonResponse(data)


@login_required(login_url='/log-in')
def getPlayer2(request, room_name):
    ROOM = Room.objects.get(room_name=room_name)
    player2Name = ROOM.player2
    data = {
        'player2Name': str(player2Name)
    }
    return JsonResponse(data)


@login_required(login_url='/log-in')
def recordScores(request, room_name):
    if (request.method == 'POST'):
        receivedData = json.loads(request.body)
        ROOM = Room.objects.get(room_name=room_name)
        ROOM.score_player1 = receivedData['scorePlayer1']
        ROOM.score_player2 = receivedData['scorePlayer2']
        ROOM.save()
        data = {'isScoreSaved': True}
        return JsonResponse(data)
    return redirect('room', room_name)
