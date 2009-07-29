from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from django.db.models import Q

from cfda.models import ProgramDescription
from budget_capture.models import * 


class CFDAForm(ModelForm):
    
    class Meta():
        model = ProgramDescription
        
class BudgetDataForm(ModelForm):
    
    citation = forms.URLField(widget=forms.TextInput(attrs={'size':'40'})) 
    transactional_data_available = forms.URLField(widget=forms.TextInput(attrs={'size':'40'})) 

    class Meta():
        model = BudgetData
        
BudgetDataFormset = inlineformset_factory(BudgetData, BudgetDataFiscalYear, extra=10, max_num=10, can_delete=True)

@login_required
def main(request):
    
    tasks = Task.objects.all()
    
    return render_to_response('budget_capture/main.html', { 'tasks':tasks, 'user':request.user})


@login_required
def task(request, task_id):
    
    task = Task.objects.get(id=task_id)
    
    items = Item.objects.filter(task=task)
    
    pending_items = []
    
    for item in items:
        
        if item.budgetdata_set.filter(user=request.user).count() == 0:
            pending_items.append(item)
            
    reviewed_items = BudgetData.objects.filter(user=request.user)
        
    return render_to_response('budget_capture/task.html', { 'task':task, 'pending_items':pending_items, 'reviewed_items':reviewed_items, 'user':request.user})

@login_required
def capture(request, item_id):
    
    item = Item.objects.get(id=item_id)
    
    if request.method == 'POST':
        
        form = BudgetDataForm(request.POST) 
    
        if form.is_valid():
            form.instance.item = item
            form.instance.user = request.user
            form.save()
            
            return HttpResponseRedirect('/budget_capture/edit/%d/' % form.instance.id)
        
    else:
        form = BudgetDataForm()
    
    return render_to_response('budget_capture/capture.html', {'item':item, 'form':form, 'user':request.user})


@login_required
def edit(request, data_id):
    
    budget_data = BudgetData.objects.get(id=data_id)
    
    if request.method == 'POST':
        
        budgetdata_form = BudgetDataForm(request.POST, prefix='data', instance=budget_data)
        budgetdata_years_formset = BudgetDataFormset(request.POST, prefix='years', instance=budget_data)
        
        if budgetdata_form.is_valid() and budgetdata_years_formset.is_valid():
            budgetdata_form.save()
            budgetdata_years_formset.save()
        
    else:
        budgetdata_form = BudgetDataForm(instance=budget_data, prefix='data')
        budgetdata_years_formset = BudgetDataFormset(instance=budget_data, prefix='years')
    
    return render_to_response('budget_capture/edit.html', {'budget_data':budget_data, 'budgetdata_form':budgetdata_form, 'budgetdata_years_formset':budgetdata_years_formset, 'user':request.user})

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

