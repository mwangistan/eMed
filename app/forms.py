from django.forms import ModelForm
from django import forms
from .models import Staff, Patient, PatientRecord, User
from django.db.models import Q
from django.forms import extras

class LoginForm(ModelForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder':'Password'}), label='')
    
    class Meta:
        exclude = ['user', 'firstname', 'lastname', 'hospital', 'title', 'staff_id']
        model = Staff
        

    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(str(password)) < 4:
            raise forms.ValidationError("Password is too short")
        return self.cleaned_data['password']
    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
            return self.cleaned_data['username']
        except User.DoesNotExist:
            raise forms.ValidationError("Username does not exist")


class PatientSearchForm(ModelForm):
    PatientId = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                   'placeholder':'ID NO'}), label='')
    class Meta:
        exclude = ['Patientid', 'Birthcertificate_no', 'firstname', 'lastname', 'gender', 'contact', 'emergencyContact', 'county', 'date_of_birth', 'added_by']
        model = Patient
        
    def clean_PatientId(self):
        PatientId = self.cleaned_data['PatientId']
        try:
            Patient.objects.get(Q(Patientid=PatientId)| Q(Birthcertificate_no=PatientId))
            return PatientId
        except Patient.DoesNotExist:
            raise forms.ValidationError("Patient not found")
    
class PatientRecordSearch(ModelForm):
    date = forms.DateField(widget=extras.SelectDateWidget(years=range(2015, 2016)))
    class Meta:
        model = PatientRecord
        exclude = ['Patientid', 'Birthcertificate_no', 'doctorOnLastVisit', 'allergies', 'bloodGroup', 'symptoms', 'medication',
                   'Illnesses', 'surgeriesDone', 'date', 'weight', 'height', 'terminalIllness', 'lab_findings', 'lab']
            

class PatientBasicInfoForm(ModelForm):
    
    Patientid = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control',
                                                                   'placeholder':'ID Number'}), label='')
    Birthcertificate_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                   'placeholder':'Birthcertificate number'}), label='')
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                              'placeholder':'firstname'}), label='')
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                              'placeholder':'lastname'}), label='')
    contact = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                 'placeholder':'Phone no'}), label='')
    emergencyContact = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                          'placeholder':'Emergency contact'}), label='')
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget(years=range(1950, 2016)))



    def clean_Patientid(self):
            if self.cleaned_data['Patientid'] != None:
                try: 
                    patient = Patient.objects.get(Patientid=self.cleaned_data['Patientid'])
                    if patient:
                        raise forms.ValidationError("The ID number already exists")
                except Patient.DoesNotExist:
                    return self.cleaned_data['Patientid']
            return self.cleaned_data['Patientid']
        
    def clean_Birthcertificate_no(self):
        if len(str(self.cleaned_data['Birthcertificate_no'])) != 6:
            raise forms.ValidationError("The Birth certificate number is not in the correct format")
        else:
            try: 
                patient = Patient.objects.get(Birthcertificate_no=self.cleaned_data['Birthcertificate_no'])
                if patient:
                    raise forms.ValidationError("The Birth certificate number already exists")
            except Patient.DoesNotExist:
                return self.cleaned_data['Birthcertificate_no']
        
    def clean_contact(self):
        if len(str(self.cleaned_data['contact'])) != 9:
            raise forms.ValidationError("The phone number is in the wrong format")
        return self.cleaned_data['contact']
    
    def clean_emergencyContact(self):
        if len(str(self.cleaned_data['emergencyContact'])) != 9:
            raise forms.ValidationError("The phone number is in the wrong format")
        return self.cleaned_data['emergencyContact']
    
    def clean_address(self):
        if len(str(self.cleaned_data['address'])) != 5:
            raise forms.ValidationError("The postal address is incorrect")
        return self.cleaned_data['address']
    
    class Meta:
        exclude = ['Patientid', 'Birthcertificate_no', 'firstname', 'lastname', 'contact', 'emergencyContact', 'date_of_birth', 'added_by']
        model = Patient

class PatientEditForm(ModelForm):
    Patientid = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'placeholder':'ID NO'}))
    Birthcertificate_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                   'placeholder':'Birthcertificate number'}))
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                              'placeholder':'firstname'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                              'placeholder':'lastname'}))
    contact = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                 'placeholder':'Phone no'}))
    emergencyContact = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                          'placeholder':'Emergency contact'}))
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget(years=range(1950, 2016)))


    def clean_Patientid(self):
            if self.cleaned_data['Patientid'] != None:
                if len(str(self.cleaned_data['Patientid'])) != 8:
                    raise forms.ValidationError("ID number is too short")
                try: 
                    patient = Patient.objects.get(Patientid=self.cleaned_data['Patientid'])
                    if patient:
                        raise forms.ValidationError("The ID number already exists")
                except Patient.DoesNotExist:
                    return self.cleaned_data['Patientid']
            return self.cleaned_data['Patientid']

    def clean_Birthcertificate_no(self):
        if len(str(self.cleaned_data['Birthcertificate_no'])) != 6:
            raise forms.ValidationError("Enter correct Birth certificate number")

        return self.cleaned_data['Birthcertificate_no']
    
    def clean_contact(self):
        if len(str(self.cleaned_data['contact'])) != 9:
            raise forms.ValidationError("The phone number is in the wrong format")
        return self.cleaned_data['contact']
    
    def clean_emergencyContact(self):
        if len(str(self.cleaned_data['emergencyContact'])) != 9:
            raise forms.ValidationError("The phone number is in the wrong format")
        return self.cleaned_data['emergencyContact']
    
    def clean_address(self):
        if len(str(self.cleaned_data['address'])) != 5:
            raise forms.ValidationError("The postal address is incorrect")
        return self.cleaned_data['address']
    
    class Meta:
        exclude = ['Patientid', 'Birthcertificate_no', 'firstname', 'lastname', 'contact', 'emergencyContact', 'date_of_birth', 'added_by']
        model = Patient
        
class PatientRecordForm(ModelForm):
    symptoms = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control',
                                                             'placeholder':'SYMPTOMS'}), label='')
    allergies = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control',
                                                             'placeholder':'ALLERGIES (IF ANY)'}), label='')
    illness = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control',
                                                             'placeholder':'ILLNESS'}), label='')
    bloodGroup = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control',
                                                               'placeholder':'BLOOD GROUP'}), label='')
    height = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control',
                                                                'placeholder':'HEIGHT(CM)'}), label='')
    weight = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control',
                                                                'placeholder':'WEIGHT(KGS)'}), label='')
    terminalIllness = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control',
                                                                   'placeholder':'TERMINAL ILLNESSES(IF ANY)'}), label='')
    surgeriesDone = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control',
                                                                 'placeholder':'SURGERIES DONE(IF ANY)'}), label='')
    medication = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control',
                                                             'placeholder':'MEDICATION'}), label='')
    
    class Meta:
        exclude = ['Patientid', 'doctorOnLastVisit', 'allergies', 'bloodGroup', 'symptoms', 'medication',
                   'Illnesses', 'Birthcertificate_no', 'surgeriesDone', 'date', 'weight', 'height', 'terminalIllness', 'lab_findings']
        model = PatientRecord
    
