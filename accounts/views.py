from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
#user verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
#token
from django.contrib.auth.tokens import default_token_generator
#send email
from django.core.mail import EmailMessage

def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            username=email.split("@")[0]
            country=form.cleaned_data['country']
            password=form.cleaned_data['password']
            user=Account.objects.create_user(phone_number=phone_number,first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.country=country
            user.save()
            #user activation after user get saved
            #first get the current_site
            current_site=get_current_site(request)
            kuku="Please activate your account"
            mummy=render_to_string('accounts/verify_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),   #this mean encode the user.id, so nobody can see the primary key, when the account activated, we will decode it
                'token':default_token_generator.make_token(user),  #make_token is function, default_token_generator is library, make token for particular user
            })
            apalah=email
            salah=EmailMessage(kuku,mummy,to=[apalah])
            salah.send()
            x=4
            # messages.success(request,'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it. ')
            # return render(request,'accounts/login.html',{'x':x})
            return redirect('/accounts/login/?command=kuchai&email='+email)
    else:
        form=RegistrationForm()
    return render(request,'accounts/register.html',{"form":form})

def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)   #look at the accounts.models.py, the USERNAME_FIELD=email, which mean login use email
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid email or password')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'home/dashboard.html')

@login_required(login_url='login')
def logout(request):
    if request.method=="GET":   #this is just practice, remember in your own project, logout must use POST method
        auth.logout(request)
        messages.warning(request,"You are logged out")
        return redirect('login')

def activate(request,girl,boy):
    try:
        uid=urlsafe_base64_decode(boy).decode()   #decode the uidb64
        user=Account._default_manager.get(id=uid)  #get the user
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):    #if the error is occur, let the user become none
        user=None
    if user is not None and default_token_generator.check_token(user,girl): #check the token and the user then active it
        user.is_active=True
        user.save()
        messages.success(request,"Congratulation, your account is activated.")
        return redirect('login')
    else:
        messages.warning(request,"Invalid activation link")
        return redirect("register")

def forgotpassword(request):
    if request.method == "POST":
        email=request.POST['email']
    #then check the email exist or not
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            #reset password
            current_site=get_current_site(request)
            bird="Reset your password"
            kaki=render_to_string('accounts/resetpass.html',{
                'user':user,
                'domain':current_site,
                'goku':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)    #generate token for user
            })
            e=email
            send_email=EmailMessage(bird,kaki,to=[e])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.info(request,"Invalid email")
            return redirect('login')
    else:
        return render(request,'accounts/forgotpass.html')

def resetpassvalid(request,babi,salam):
    try:
        decoder=urlsafe_base64_decode(babi).decode()    #decode it and get the user
        user=Account._default_manager.get(id=decoder)   #get the user
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,salam):    #check the token is clicked or not, and user is existed,
        request.session['seven']=decoder  #okay, since the user has been decoded, so we need pass the user to the session and name it as seven, so now the session of HTTP got a file known as seven, inside got the user info
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'The link has been expired')
        return redirect('login')

def resetpassword(request):
    if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if confirm_password != password:
            messages.error(request,"Please enter same password")
            return redirect('resetpassword')
        else:
            kucing=request.session.get('seven') #get the session from the HTTP, looking the file name as seven
            user=Account.objects.get(id=kucing)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successful")
            return redirect('login')
    else:
        return render(request,'accounts/resetpassword.html')
