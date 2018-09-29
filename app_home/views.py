from django.contrib.auth.hashers import make_password, check_password
from app_home import models, forms
from django.shortcuts import render, redirect

# Create your views here.

# 主页
from app_home.models import User


def home(request):
    return render(request, 'app_home/home.html', locals())


# 登录
def login(request):
    if request.session.get('is_login', None):
        return redirect("home")
    if request.method == 'GET':
        login_form = forms.UserForm()
        return render(request, 'app_home/login.html', locals())
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        # error_email = "请检查填写的邮箱！"
        # error_password = "请检查填写密码！"
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('home')
                else:
                    error_password = "密码不正确！"
            except:
                error_email = "用户不存在！"
        return render(request, 'app_home/login.html', locals())


# 注册
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect("/index/")
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'app_home/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'app_home/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'app_home/register.html', locals())

            new_user = models.User()
            new_user.name = username
            new_user.password = make_password(password1)
            new_user.email = email
            new_user.save()
            # password = make_password(password1) # 对密码进行加密
            # User.objects.create(name=username, password=password, email=email)
            return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'app_home/register.html', locals())


# 注销
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("home")
    request.session.flush()
    return redirect("home")
