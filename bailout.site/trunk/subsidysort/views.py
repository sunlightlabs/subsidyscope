from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.forms import ModelForm
from django.db.models import Q

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
def review(request, task_id, show='all', tag_id=None, tag_location=None):
    
    task = Task.objects.get(id=task_id)
    
    items = Item.objects.filter(task=task)
    
    final_items = []
    
    if show == 'all':
        final_items = items
        
    else:
        
        for item in items:
            
            votes = item.getVotes()
            
            if show == 'yes' and votes.has_key('yes') and len(votes) == 1: 
                final_items.append(item)
            elif show == 'no' and votes.has_key('no') and len(votes) == 1:
                final_items.append(item)    
            elif show == 'split' and len(votes) > 1:
                final_items.append(item)
         
    selected_tag = None

    try:
        tag_location = int(tag_location)
    except:
        tag_location = -1
    
    if tag_id and int(tag_id):
        
        tag_id = int(tag_id)
        
        selected_tag = Tag.objects.get(id=tag_id)
        
        final = User.objects.get(id=14)
        
        
            
        if tag_location == 1:
            final_items = Item.objects.filter(Q(vote__user=final) & Q(vote__primary_purpose=selected_tag))
        elif tag_location == 2:
            final_items = Item.objects.filter(Q(vote__user=final) & Q(vote__tags=selected_tag))
        else:
            final_items = Item.objects.filter(Q(vote__user=final) & (Q(vote__primary_purpose=selected_tag) | Q(vote__tags=selected_tag)))    
      
    
    tags = Tag.objects.all()

    return render_to_response('subsidysort/review.html', {'task':task, 'items':final_items, 'user':request.user, 'tags':tags, 'selected_tag':selected_tag, 'tag_location':tag_location } )
                            


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
        
#        for item in items:
#            if item.vote_set.filter(user=request.user).count() == 0:
#                return HttpResponseRedirect('/subsidysort/vote/%d/' % item.id)
#        
        return HttpResponseRedirect('/subsidysort/review/%d/' % item.task.id)
    
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

