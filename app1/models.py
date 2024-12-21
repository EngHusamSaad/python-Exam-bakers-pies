from django.db import models
import re
from datetime import datetime


# Create your models here.


class BakerManger(models.Manager):
    def baker_validator(self,formdata,index):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if index=="register":
            if len(formdata["first_name"]) <2:
                errors['first_name']="First Name should be at least 2 Chars"
            if len(formdata["last_name"]) <2:
                errors['last_name']="Last Name should be at least 2 Chars"
                
            if len(formdata["password"]) <8:
                errors['password']="password should be at least 8 Chars"
                
            if (formdata["password"]) != formdata["confirm_password"]:
                errors['password']="Password should be Match ,,, !"
                
            if not EMAIL_REGEX.match(formdata['email']):  
                errors['email'] = "Invalid email address!"
                
            if not formdata["first_name"].isalpha():
                errors['first_name'] = "Invalid First Name ONly Chars !"
                
            if not formdata["last_name"].isalpha():
                errors['last_name'] = "Invalid Last Name ONly Chars !"
                
            if Baker.objects.filter(email=formdata["email"]).exists():
                errors["email_exist"]="Email should be uniqe !"
            
                
    
        return errors

class PieManger(models.Manager):
    def pie_validator(self,formdata):
        errors={}
        if Pie.objects.filter(name=formdata["name"]).exists():
                errors["name"]="Name of Pie should be uniqe !"
                
        return errors
                

   
   
class Baker(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=BakerManger()
     
class Pie(models.Model):
    name=models.CharField(max_length=50)
    filling=models.CharField(max_length=50)
    crust=models.CharField(max_length=50)
    votes=models.IntegerField(null=True,default=0)
    baker=models.ForeignKey(Baker,related_name="pies",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=PieManger()
    

    