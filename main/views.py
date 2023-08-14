from django.shortcuts import redirect, render
from django.utils import timezone
from main.models import Member
from dobby.models import File
from django.contrib import messages

# HOME
def main(request):
    # s_id = request.session.get('s_id') # session id 유무 체크
    # if s_id==None:
    #     return redirect("/main/login/")
    
    return render(request,"main/main.html")
# def main(request):
#     return render(request,"main/main.html")

# SIGNUP
def signup(request):   
    if request.method == "GET":
        return render(request, "main/signup.html")
    
    elif request.method == "POST":
        form = Member(member_id=request.POST['member_id'], member_email=request.POST['member_email'],
                      member_password=request.POST['member_password'], member_joindate=timezone.localtime(),
                      member_nick=request.POST['member_nick'], member_status=0,
                    )
        form.save()
    return redirect("/main/login/")

# LOGIN
def login(request):

    if request.method == "GET":
        return render(request, "main/login.html")
    
    elif request.method == "POST":
        in_id = request.POST['member_id']
        in_pw = request.POST['member_password']        

        try:
            out_id = Member.objects.get(member_id=in_id)
        except Member.DoesNotExist:
            out_id = None
            messages.info(request, '아이디 혹은 비밀번호를 확인해주세요.')
            return render(request, 'main/login.html')
        
        if out_id is None:        
            return render(request, "main/login.html")
        else:
            if in_pw == out_id.member_password:
                request.session['s_id'] = in_id
        
    return redirect("/main/main/")

# LOGOUT
def logout(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    request.session.flush()
    
    return redirect("/main/login/")


# MY PAGE
def my(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    files = File.objects.all()
    
    return render(request,"main/my.html", {'files' : files})
