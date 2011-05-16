from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.forms import ModelForm
from django.db.models import Q

from django import forms

from cfda.models import ProgramDescription, ProgramFunctionalIndex
from budget_accounts.models import BudgetFunction
from sectors.models import Sector
from subsidysort.models import * 

    
class SectorForm(ModelForm):
    
    budget_functions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=BudgetFunction.objects.all(), required=False)
    functional_indexes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=ProgramFunctionalIndex.objects.all(), required=False)
    
    class Meta:
        model = Sector
        fields = ['budget_functions', 'functional_indexes']

#@login_required
def main(request):
    
     sectors = Sector.objects.all()
          
     return render_to_response('subsidysort/main.html', {'sectors':sectors})

#@login_required
def sector(request, sector_id):
    
    sector = Sector.objects.get(pk=int(sector_id))

    included_programs = sector.programdescription_set.all().distinct()
    import logging
    logging.debug(included_programs) 
    bf_list = sector.budget_functions.all()
   
    all_programs_data = {}
    all_programs = []
    #each key maps to a tuple
    #the tuple order is (budget function or functional index?, which ones?)
     
    for bf in bf_list:
        bf_programs = ProgramDescription.objects.filter(budget_accounts__budget_function=bf).distinct()
        for bf_prog in bf_programs:
            if all_programs_data.has_key(bf_prog):
                p = all_programs_data[bf_prog]
                p[1] = p[1] + ', ' + bf.name + '(bf)'
            else:
                all_programs_data[bf_prog] = ['budget function', bf.name + '(bf)']
                all_programs.append(bf_prog)
        
    fi_list = sector.functional_indexes.all()
    
    for fi in fi_list:
        fi_programs = ProgramDescription.objects.filter(functional_index=fi).distinct()
        for fi_prog in fi_programs:
            if all_programs_data.has_key(fi_prog):
                p = all_programs_data[fi_prog]
                if p[0] == 'budget function':
                    p[0] = 'both'
                p[1] += ', '+ fi.name + '(fi) '
            else:
                all_programs_data[fi_prog] = ['functional index', fi.name + '(fi)']
                all_programs.append(fi_prog)     
   
    data = []
    for p in all_programs:
        data.append((p, all_programs_data[p][0], all_programs_data[p][1]))
    
    return render_to_response('subsidysort/sector.html', {'sector':sector, 'included_programs':included_programs, 'all_programs': all_programs, 'all_programs_data': all_programs_data, 'data': data })

#@login_required
def sector_edit(request, sector_id):
    
    sector = Sector.objects.get(pk=int(sector_id))

    if request.method == 'POST':
        form = SectorForm(request.POST, instance=sector)
        form.save()
    else:
        form = SectorForm(instance=sector)
    
    return render_to_response('subsidysort/sector_edit.html', {'sector':sector, 'form':form})

#@login_required
def sector_add(request, sector_id, program_id):
    
    sector = Sector.objects.get(pk=int(sector_id))
    
    program = ProgramDescription.objects.get(pk=int(program_id))

    if request.method == 'POST':
        program.sectors.add(sector)
    
    return HttpResponse()

#@login_required
def sector_delete(request, sector_id, program_id):
    
    sector = Sector.objects.get(pk=int(sector_id))
    
    program = ProgramDescription.objects.get(pk=int(program_id))

    if request.method == 'POST':
        program.sectors.remove(sector)
    
    return HttpResponse()

#@login_required
def sector_search(request, sector_id, cfda):
    
    sector = Sector.objects.get(pk=int(sector_id))
    
    included_programs = sector.programdescription_set.all()
    
    try:
        program = ProgramDescription.objects.get(program_number=cfda.strip())
    
        if program in included_programs:
            included = True
        else:
            included = False
        
    except:
        program = False
        included = False
        
    
    
    return render_to_response('subsidysort/cfda_search.html', {'program':program, 'included':included})


#@login_required
def cfda(request, program_id):
    
    program = ProgramDescription.objects.get(id=int(program_id))
    
    return render_to_response('subsidysort/cfda.html', {'program':program})



#@login_required
def cfda_save_comment(request, program_id):
    
    program = ProgramDescription.objects.get(id=int(program_id))
    
    if request.method == 'POST':
        program.scoping_comment = request.POST['comment']
        program.save()
    
    return HttpResponse()



def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            if request.POST.has_key('next'):
                return HttpResponseRedirect(request.POST['next'])
            else:
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

