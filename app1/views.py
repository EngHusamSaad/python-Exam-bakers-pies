from django.shortcuts import render,redirect,HttpResponse
from app1.models import *
from django.contrib import messages
import bcrypt



# Create your views here.


def index(request):
    return render(request,"index.html")



def register(request):
    errors_add=Baker.objects.baker_validator(request.POST,"register")
    if len(errors_add) >0:
        for key,value in errors_add.items():
            messages.error(request,value,extra_tags="add_error")
            
    else:
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        password=request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_baker=Baker.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash)         
        
    return redirect("/")


def login(request):
    
    
    if request.method =="GET":
        user_login=Baker.objects.get(email=request.session['email'])
        all_pies_baker = Pie.objects.filter(baker=user_login)
        data={
            "first_name":user_login.first_name,
            "baker_pies":user_login.pies,
            "baker_id" : request.session['baker_id'],
            "all_pies_baker" :all_pies_baker,    
                }
                    
        return render(request, "dashboard.html", data) 
    
    if request.method =="POST":
        errors_add=Baker.objects.baker_validator(request.POST,"login")
        if len(errors_add) >0:
            for key,value in errors_add.items():
                messages.error(request,value,extra_tags="login_error")
        else:
                    
            email=request.POST["login_email"] 
            password=request.POST["login_password"] 
                 
            
            try:
                user_login=Baker.objects.get(email=email)
                request.session['baker_id'] = user_login.id
                request.session['email'] = email
                all_pies_baker = Pie.objects.filter(baker=user_login)
                data={
                    "first_name":user_login.first_name,
                    "baker_pies":user_login.pies,
                    "baker_id" : request.session['baker_id'],
                    "all_pies_baker" :all_pies_baker,    
                }
                if bcrypt.checkpw(password.encode(), user_login.password.encode()):
                    
                    return render(request, "dashboard.html", data) 
                else:
                    messages.error(request,"Password Wrong !",extra_tags="login_error")
                    print("Password Wrong") 
                    return redirect("/")
            except :
                messages.error(request,"Email is Not Exist",extra_tags="login_error")
                print("email Not Found")
                return redirect("/")
    else:
        return HttpResponse("Forbidden access Page !")



def new_pies(request,baker_id):
    
    errors=Pie.objects.pie_validator(request.POST)
    
    if len(errors) >0:
        for key,value in errors.items():
            messages.error(request,value)
            
        
    
    else:

         name = request.POST["name"]
         filling = request.POST["filling"]
         crust = request.POST["crust"]
         baker=Baker.objects.get(id=baker_id)
         new_pie = Pie.objects.create(name=name, filling=filling, crust=crust,baker=baker )
    return redirect("/login")




def delete_pie(request):
    pie_id = request.POST["pie_id"]
    pie = Pie.objects.get(id=int(pie_id))
    pie.delete()
    return redirect("/login")



def all_pies(request):
        data = {
            "all_pies": Pie.objects.all(),
            }
        return render(request, "all_pies.html",data) 


def pie_card(request,pie_id):
    pie=Pie.objects.get(id=pie_id)
    
    data={
        "pie":pie,  
    }
    return render(request, "pie_card.html",data) 



def vote_pie(request,pie_id):
    
    if request.method =="POST":
        pie=Pie.objects.get(id=pie_id)
        pie.votes=int(pie.votes)+1
        pie.save()
        
        return redirect ("all_pies")
    
    else:
        return HttpResponse(" Access denied , Forbidden !")
    
    
def edit_pie(request,pie_id):
    pie=Pie.objects.get(id=pie_id)
    
    data={
        "pie":pie,
    }
    
    return render(request, "edit_pie.html",data) 



def update_pie(request):
    
    if request.method =="POST":
        pie_id = request.POST["pie_id"]
        pie_name = request.POST["name"]
        filling = request.POST["filling"]
        crust = request.POST["crust"]
        
        pie=Pie.objects.get(id=pie_id)
        
        pie.name=pie_name
        pie.filling=filling
        pie.crust=crust
        
        pie.save()
        
        return redirect ("login")
    
    
def logout(request):
    if 'baker_id' in request.session:
        del request.session['baker_id']
        
    return render(request,"index.html")


    
    
