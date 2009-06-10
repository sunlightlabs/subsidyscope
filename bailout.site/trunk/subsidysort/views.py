from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.forms import ModelForm

from cfda.models import ProgramDescription
from subsidysort.models import * 

class VoteForm(ModelForm):
    
    class Meta():
        model = Vote
        
class CFDAForm(ModelForm):
    
    class Meta():
        model = ProgramDescription
         

@login_required
def main(request):
    
    tasks = Task.objects.all()
    
    return render_to_response('subsidysort/main.html', { 'tasks':tasks, 'user':request.user})

@login_required
def task(request, task_id):
    
    task = Task.objects.get(id=task_id)
    
    items = Item.objects.filter(task=task)
    
    pending_items = []
    
    for item in items:
        
        if item.vote_set.filter(user=request.user).count() == 0:
            pending_items.append(item)
        
    votes = Vote.objects.filter(user=request.user, item__task=task)
    
    return render_to_response('subsidysort/task.html', { 'task':task, 'pending_items':pending_items,'votes':votes, 'user':request.user})

@login_required
def vote(request, item_id):
    
    item = Item.objects.get(id=item_id)
    
    if request.method == 'POST':
        try:
            vote = item.vote_set.get(user=request.user)
            vote = VoteForm(request.POST, instance=vote)
        except:
            vote = VoteForm(request.POST) 
    
        vote.instance.item = item
        vote.instance.user = request.user
        vote.save()
        
        items = Item.objects.filter(task=item.task)
        
        for item in items:
            if item.vote_set.filter(user=request.user).count() == 0:
                return HttpResponseRedirect('/subsidysort/vote/%d/' % item.id)
        
        return HttpResponseRedirect('/subsidysort/task/%d/' % item.task.id)
    
    try:    
        vote = item.vote_set.get(user=request.user)
        vote_form = VoteForm(instance=vote)
    except: 
        vote_form = VoteForm()
    
    return render_to_response('subsidysort/vote.html', {'item':item, 'vote_form':vote_form, 'user':request.user})

@login_required
def cfda(request, cfda_id):
    
    program = ProgramDescription.objects.get(id=int(cfda_id))
    
    return render_to_response('subsidysort/cfda.html', {'program':program, 'user':request.user})


def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return HttpResponseRedirect('/subsidysort/')
        
        else:
            return render_to_response('subsidysort/login.html', {'invalid':True})
    else:
        return render_to_response('subsidysort/login.html')  

def logout(request):
    
    logout_auth(request)
    return render_to_response('subsidysort/login.html')

def change_password(request):
    
    pass 

