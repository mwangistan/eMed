import re
from django.shortcuts import render
from .forms import *
from .models import Staff, Patient, PatientRecord
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def staffLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            request.session['password'] = form.cleaned_data['password']
            
            staff = authenticate(username=username, password=password)
            if staff is not None:
                login(request, staff)
                return HttpResponseRedirect('/profile/search/')
            else:
                return HttpResponseRedirect('/')
        else:
            return render(request, 'home.html', {'form':form})
    else:
        form = LoginForm()
        return render(request, 'home.html', {'form':form})

def staffLogout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/')
def patientSearch(request):
    #get profile
    profile = request.user.get_profile()
    
    #if staff is receptionist
    if re.search("Rec", str(profile)):
        
        if request.method == 'POST':
            form = PatientSearchForm(request.POST)
            
            if form.is_valid():
                if form.cleaned_data['PatientId'] == None:
                    patient = Patient.objects.get(Birthcertificate_no=form.cleaned_data['PatientId'])
                patient = Patient.objects.get(Q(Patientid=form.cleaned_data['PatientId'])|
                                                      Q(Birthcertificate_no=form.cleaned_data['PatientId']))
        
                request.session['patient'] = form.cleaned_data['PatientId']
                request.session.set_expiry(300)
                
                return render(request, 'receptionist.html', {'patient':patient, 'form':form, 'profile':profile})
            else:
                pform = PatientBasicInfoForm()
                return render(request, 'receptionist.html', {'profile':profile, 'form':form, 'pform':pform})
                
        else:
            form = PatientSearchForm()
            return render(request, 'receptionist.html', {'profile':profile, 'form':form})
        
    #if staff is doctor
    if re.search("Dr", str(profile)):
        if request.method == 'POST':
        
            form = PatientSearchForm(request.POST)
            pform = PatientRecordForm()
               
            if form.is_valid():  
                patient_details = Patient.objects.get(Q(Patientid=form.cleaned_data['PatientId'])|
                                                      Q(Birthcertificate_no=form.cleaned_data['PatientId']))
                
                request.session['patient'] = form.cleaned_data['PatientId']
                request.session.set_expiry(300)
                
                try: 
                    patient_records = PatientRecord.objects.filter(Q(Patientid=patient_details) |
                                                                   Q(Birthcertificate_no=patient_details))
                    patient = patient_records.latest('date')
                
                    
                    bloodgroup = []
                    height = []
                    weight = []
                    
                    for patient in patient_records:
                        for i in [patient.bloodGroup]:
                            bloodgroup.append(i)
                            bloodgroup = filter(None, bloodgroup)
                    for patient in patient_records:
                        for i in [patient.height]:
                            height.append(i)
                            height = filter(None, height)
                    for patient in patient_records:
                        for i in [patient.weight]:
                            weight.append(i)
                            weight = filter(None, weight)
                    
                    
                    if bloodgroup == [] or weight == [] or height == []:
                        return render(request, 'doctor.html', {'profile':profile, 'form':form, 'patient_details':patient_details,
                                                       'patient_records':patient_records, 'pform':pform, 
                                                       'patient':patient})  
                        
                    return render(request, 'doctor.html', {'profile':profile, 'form':form, 'patient_details':patient_details,
                                                       'patient_records':patient_records,
                                                       'pform':pform, 'patient':patient, 'bloodgroup':bloodgroup,
                                                       'height':height, 'weight':weight})
                except PatientRecord.DoesNotExist:
                    pform = PatientRecordForm()
                    return render(request, 'doctor.html', {'profile':profile, 'form':form, 'patient_details':patient_details, 
                                                       'pform':pform})

                
            else:
                return render(request, 'doctor.html', {'profile':profile, 'form':form})
            
        else:
            form = PatientSearchForm()
            return render(request, 'doctor.html', {'profile':profile, 'form':form})
            

@login_required(login_url='/')
def addPatient(request):
    #used for logging activities
    profile = request.user.get_profile()
    username = request.user.get_username()
    
    form = PatientSearchForm()
    
    if request.method == 'POST':
        pform = PatientBasicInfoForm(request.POST)
        
        if pform.is_valid():
            Patientid = pform.cleaned_data['Patientid']
            Birthcertificate_no = pform.cleaned_data['Birthcertificate_no']
            firstname = pform.cleaned_data['firstname']
            lastname = pform.cleaned_data['lastname']
            contact = pform.cleaned_data['contact']
            emergencyContact = pform.cleaned_data['emergencyContact']
            date_of_birth = pform.cleaned_data['date_of_birth']
            county = pform.cleaned_data['county']
            gender = pform.cleaned_data['gender']
            
            staff_instance = Staff.objects.get(staff_id=username)
            p = Patient(Patientid=Patientid, firstname=firstname, lastname=lastname, contact=contact, emergencyContact=
                        emergencyContact, date_of_birth=date_of_birth, county=county, added_by=staff_instance,
                        gender=gender, Birthcertificate_no=Birthcertificate_no)
            p.save()
            
            patient = Patient.objects.get(Q(Patientid=Patientid) | Q(Birthcertificate_no=Birthcertificate_no))
            return render(request, 'receptionist.html', {'patient':patient, 'profile':profile, 'form':form})
        else:
            return render(request, 'receptionist.html', {'pform':pform, 'profile':profile, 'form':form})
    else:
        pform = PatientBasicInfoForm()
        return render(request, 'receptionist.html', {'pform':pform, 'profile':profile, 'form':form})
    
@login_required(login_url='/')
def updateRecord(request):
    
    profile = request.user.get_profile()
    username = request.user.get_username()
    
    form = PatientSearchForm()
    
    if request.method == 'POST':
        pform = PatientRecordForm(request.POST)
        
        if pform.is_valid():
            symptoms = pform.cleaned_data['symptoms']
            allergies = pform.cleaned_data['allergies']
            illness = pform.cleaned_data['illness']
            bloodGroup = pform.cleaned_data['bloodGroup']
            height = pform.cleaned_data['height']
            weight = pform.cleaned_data['weight']
            terminalIllness = pform.cleaned_data['terminalIllness']
            surgeriesDone = pform.cleaned_data['surgeriesDone']
            medication = pform.cleaned_data['medication']
            lab = pform.cleaned_data['lab']
            doctorOnLastVisit = Staff.objects.get(staff_id=username)
            
            if len(str(request.session['patient'])) == 6:
                Birthcertificate_no = request.session['patient']
                p = PatientRecord(symptoms=symptoms, allergies=allergies, Illnesses=illness, bloodGroup=bloodGroup,
                              height=height, weight=weight, terminalIllness=terminalIllness, 
                              surgeriesDone=surgeriesDone, medication=medication, doctorOnLastVisit=doctorOnLastVisit,
                              lab=lab, Birthcertificate_no=Patient.objects.get(Birthcertificate_no=Birthcertificate_no)
                              
                              )
                p.save()
                
            else: 
                Patientid = request.session['patient']
                patient = Patient.objects.get(Patientid=Patientid)
                Birthcertificate_no = patient.Birthcertificate_no
    

                p = PatientRecord(symptoms=symptoms, allergies=allergies, Illnesses=illness, bloodGroup=bloodGroup,
                              height=height, weight=weight, terminalIllness=terminalIllness, 
                              surgeriesDone=surgeriesDone, medication=medication, doctorOnLastVisit=doctorOnLastVisit,
                              lab=lab, Patientid=Patient.objects.get(Patientid=Patientid), 
                              Birthcertificate_no=Patient.objects.get(Birthcertificate_no=Birthcertificate_no)
                              
                              )
            
                p.save()
        
            patient_details = Patient.objects.get(Q(Patientid=request.session['patient']) | 
                                                  Q(Birthcertificate_no=request.session['patient']))
            
            patient_records = PatientRecord.objects.filter(Q(Patientid=patient_details) |
                                                           Q(Birthcertificate_no=patient_details))
            
            return render(request, 'doctor.html', {'form':form, 'profile':profile,
                                                   'patient_records':patient_records,
                                                   'patient_details':patient_details})
        else:
            return render(request, 'doctor.html', {'form':form, 'profile':profile})
    
    else:
        form = PatientRecordForm() 
        return render(request, 'doctor.html', {'form':form, 'profile':profile})
    
@login_required(login_url='/')
def medicalHistory(request):
    
    profile = request.user.get_profile()
    form = PatientSearchForm()
    sform = PatientRecordSearch()
    
    try:
        request.session['patient']
        patient = Patient.objects.get(Q(Patientid=request.session['patient']) |
                                      Q(Birthcertificate_no=request.session['patient']))
        
        patient_records = PatientRecord.objects.filter(Q(Patientid=patient) |
                                                       Q(Birthcertificate_no=patient)).order_by('-date')
        
        patient_records = mk_paginator(request, patient_records, 6)
    
        return render(request, 'medical.html', {'form':form, 'profile':profile, 'patient_records':patient_records,
                                            'patient_details':patient, 'sform':sform})
    except:
        return render(request, 'medical.html', {'form':form, 'profile':profile})

@login_required(login_url='/')
def medicalDetails(request, pk):
    profile = request.user.get_profile()
    form = PatientSearchForm()
    
    patient = PatientRecord.objects.get(pk=int(pk))

    return render(request, 'medicalDetail.html', {'patient':patient, 'form':form, 'profile':profile})

@login_required(login_url='/')
def medicalSearch(request):
    if request.method == 'POST':
        return(request, 'medical.html')
    else:
        form = PatientRecordSearch()
        return(request, 'medical', {'form':form})
    
@login_required(login_url='/')
def editPatient(request):
    username = request.user.get_username()
    profile = request.user.get_profile()
    
    patient = Patient.objects.get(Q(Patientid=request.session['patient']) | Q(Birthcertificate_no=request.session['patient']))
    form = PatientSearchForm(initial={'PatientId':patient.Patientid})
    
    if request.method == 'POST':
        eform = PatientEditForm(request.POST, instance=patient)
        if eform.is_valid():
            
            patient.Patientid = eform.cleaned_data['Patientid']
            patient.Birthcertificate_no = eform.cleaned_data['Birthcertificate_no']
            patient.firstname = eform.cleaned_data['firstname']
            patient.lastname = eform.cleaned_data['lastname']
            patient.contact = eform.cleaned_data['contact']
            patient.emergencyContact = eform.cleaned_data['emergencyContact']
            patient.date_of_birth = eform.cleaned_data['date_of_birth']
            patient.county = eform.cleaned_data['county']
            patient.gender = eform.cleaned_data['gender']
            
            staff_instance = Staff.objects.get(staff_id=username)
            
            patient.added_by = staff_instance
            patient.save()
            patient = Patient.objects.get(Birthcertificate_no=patient.Birthcertificate_no)
            return render(request, 'receptionist.html', {'form':form, 'patient':patient})
        else:
            return render(request, 'receptionist.html', {'form':form, 'eform':eform, 'profile':profile})
    else:
        eform = PatientEditForm(initial={'Patientid':patient.Patientid, 'firstname':patient.firstname,
                                         'lastname':patient.lastname, 'contact':patient.contact,
                                         'emergencyContact':patient.emergencyContact,
                                         'date_of_birth':patient.date_of_birth, 
                                         'Birthcertificate_no':patient.Birthcertificate_no}, instance=patient)
        return render(request, 'receptionist.html', {'form':form, 'eform':eform, 'profile':profile})
    
    