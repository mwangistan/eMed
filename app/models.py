from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import validators


GENDER = (
                 ('Male', 'Male'),
                 ('Female', 'Female'),
                 
                 )

EXAMS = (
         ('General', 'general'),
         ('Eyes', 'Eyes'),
         ('Ear/Nose/Throat', 'Ear/Nose/Throat'),
         ('Cardiovascular', 'Cardiovascular'),
         ('Gastrointestinal', 'Gastrointestinal'),
         ('Genitourinary', 'Genitourinary'),
         ('Musculoskeletal', 'Musculoskeleteal'),
         ('Skin', 'Skin'),
         ('Neurologic','Neurologic'),
         ('Psychriatric', 'Psychiatric'),
         ('Endrocrine', 'Endocrine'),
         ('Lymphatic', 'Lymphatic'),
         ('Allergic/Immunologic', 'Allergic/Immunologic'),
       )

LOCATION = (
            ('Baringo', 'Baringo'),
            ('Bomet', 'Bomet'),
            ('Bungoma', 'Bungoma'),
            ('Busia', 'Busia'),
            ('Elgeyo', 'Elgeyo'),
            ('Embu', 'Embu'),
            ('Garissa', 'Garissa'),
            ('Homabay', 'Homabay'),
            ('Isiolo', 'Isiolo'),
            ('Kajiado', 'Kajiado'),
            ('Kericho', 'Kericho'),
            ('Kakamega', 'Kakamega'),
            ('Kwale', 'Kwale'),
            ('Kilifi', 'Kilifi'),
            ('Kitui', 'Kitui'),
            ('Kiambu', 'Kiambu'),
            ('Kirinyaga', 'Kirinyaga'),
            ('Kisumu', 'Kisumu'),
            ('Kisii', 'Kisii'),
            ('Lamu', 'Lamu'),
            ('Laikipia', 'Laikipia'),
            ('Mandera', 'Mandera'),
            ('Marsabit', 'Marsabit'),
            ('Machakos', 'Machakos'),
            ('Makueni', 'Makueni'),
            ('Migori', 'Migori'),
            ('Mombasa', 'Mombasa'),
            ('Muranga', 'Muranga'),
            ('Nakuru', 'Nakuru'),
            ('Nandi', 'Nandi'),
            ('Nairobi', 'Nairobi'),
            ('Narok', 'Narok'),
            ('Nyandarua', 'Nyandarua'),
            ('Nyamira', 'Nyamira'),
            ('Nyeri', 'Nyeri'),
            ('Samburu', 'Samburu'),
            ('Siaya', 'Siaya'),
            ('Tana river', 'Tana river'),
            ('Tharaka-Nithi', 'Tharaka_Nithi'),
            ('Transzoia', 'Transzoia'),
            ('Turkana', 'Turkana'),
            ('Wajir', 'Wajir'),
            ('Westpokot', 'Westpokot'),
            ('Uasin Gishu', 'Uasin Gishu'),
            ('Vihiga', 'Vihiga'),
            
            )
TITLES = (
          ('Dr', 'Doctor'),
          ('Rec', 'Receptionist'),
          )

def validate(value):
    try:
        Staff.objects.get(staff_id=value)
        raise forms.ValidationError("Staff ID already exists")
    except Staff.DoesNotExist:
        return value


    
class Staff(models.Model):
    user = models.ForeignKey(User, unique=True)
    firstname= models.CharField(max_length=15)
    lastname = models.CharField(max_length=15)
    staff_id = models.CharField(max_length=8, validators = [validate])
    title = models.CharField(max_length=5, choices=TITLES)
    hospital = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = 'Staff'
    
    def __unicode__(self):
        return u"%s %s %s" %(self.title, self.firstname, self.lastname)


class Patient(models.Model):
    Patientid = models.IntegerField(max_length=8, null=True, blank=True)
    Birthcertificate_no = models.IntegerField()
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    gender = models.CharField(max_length=6, choices=GENDER)
    contact = models.IntegerField()
    emergencyContact = models.IntegerField()
    county = models.CharField(max_length=20, choices=LOCATION)
    date_of_birth = models.DateField()
    added_by = models.ForeignKey(Staff)
    
    def __unicode__(self):
        return str(self.Patientid)
    


class PatientRecord(models.Model):
    Patientid = models.ForeignKey(Patient, related_name='patientrecord_id', null=True, blank=True)
    Birthcertificate_no = models.ForeignKey(Patient, related_name='patientrecord_birth')
    doctorOnLastVisit = models.ForeignKey(Staff)#Id of doctor who last searched patients details
    allergies = models.TextField(null=True, blank=True)
    bloodGroup = models.CharField(max_length=2, null=True, blank=True)
    symptoms = models.TextField()
    medication = models.TextField()
    Illnesses = models.TextField(null=True, blank=True)
    surgeriesDone = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    lab = models.CharField(max_length=20, choices=EXAMS, null=True, blank=True)
    lab_findings = models.TextField(null=True, blank=True)
    terminalIllness = models.TextField(blank=True, null=True)
    height = models.IntegerField(max_length=3, blank=True, null=True)
    weight = models.IntegerField(max_length=4, blank=True, null=True)

    def __unicode__(self):
        return str(self.Birthcertificate_no)
    
    