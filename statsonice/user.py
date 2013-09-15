from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from includes.log_event import log_event
from statsonice.models import UserInfo

def register(request):
    errors = []
    success = False
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if len(password) < 6:
            errors.append('Password is too short')
        if '@' not in email:
            errors.append('Email is improperly formatted')
        if User.objects.filter(email=email).exists():
            errors.append('Email already taken')
        if User.objects.filter(username=username).exists():
            errors.append('Username already taken')
        if len(errors) == 0:
            log_event('New User', username+' at '+email)
            user = User.objects.create_user(username, email, password)
            userinfo = UserInfo()
            userinfo.user = user
            userinfo.last_login = date.today()
            userinfo.save()
            success = True
    return render(request, 'users/register.dj', {
        'errors':errors,
        'success': success,
    })

def login(request):
    errors = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                auth_login(request, user)
                if 'next' in request.POST and request.POST['next'] != '':
                    return redirect(request.POST['next'])
                else:
                    return redirect('account')
            else:
                errors.append("Your account has been disabled")
        else:
            errors.append("Your username and password were incorrect.")
    next = 'account'
    if 'next' in request.GET:
        next = request.GET['next']
    return render(request, 'users/login.dj', {
        'errors':errors,
        'next':next,
    })

@login_required
def logout(request):
    successes = ['You have been logged out']
    auth_logout(request)
    return render(request, 'users/login.dj', {
        'successes': successes,
    })

@login_required
def account(request):
    return render(request, 'users/account.dj')

def subscribe(request):
    return render(request, 'users/subscription.dj')


@login_required
def change_account_settings(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        if request.POST['password'] != '':
            user.set_password(request.POST['password'])
        user.save()
    return render(request, 'users/change_account_settings.dj')

"""
@login_required
def payment_processing(request):
    return render(request, 'users/payment_processing.dj')

# TODO: add user input and get subscription name from it
# TODO: clean up this mess
def upgrade_account(request):
    # save features and account upgrades to use in deciding which to display to the user
    features = {'bronze':['basic search'], 'silver':['basic search','advanced search','program layout tool (save 5)'],
                'gold':['basic search','advanced search','statistics'], 'platinum':['basic search','advanced search','program layout tool (save 5)','statistics'],
                'diamond':['basic search','advanced search','program layout tool (save 50)','statistics']}
    act_upgrades = ['bronze','silver','gold','platinum','diamond']
    costs = {'bronze':0.00, 'silver':4.95, 'gold':9.95, 'platinum':12.95, 'diamond':19.95}

    # act = user.subscription.name
    act = 'silver'
    if act is 'bronze':
        span_num = 'col-3'
    else:
        span_num = 'col-4'
    act_cost = costs[act]
    act_features = features[act]
    act_upgrades = act_upgrades[act_upgrades.index(act)+1:]
    for a in act_upgrades:
        costs[a] -= act_cost
        if act != 'bronze':
            costs[a] += 0.95

    return render(request, 'users/upgrade_account.dj', {
            'act': act,
            'act_cost': act_cost,
            'act_features': act_features,
            'act_upgrades': act_upgrades,
            'costs': costs,
            'features': features,
            'span_num': span_num,
        })
"""
