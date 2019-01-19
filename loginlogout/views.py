from django.shortcuts import render
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth import get_user_model
User = get_user_model()
from . import form

# Create your views here.

def out(request):
	auth.logout(request)
	return redirect('/video/all')

def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/video/')
        else:
            args['login_error'] = 'Пользователь не найден'
            return render(request, 'log.html', args)
    else:
        return render(request, 'log.html', args)


def sign(request):
    args = {}
    args.update(csrf(request))
    args['form'] = form.UserForm
    args['url'] = "/log/register/"
    args['user'] = auth.get_user(request).username
    if request.POST:
        user = User.objects.create_user(username=request.POST.get('username', ""),
                                        email=request.POST.get('email',""),
                                        password=request.POST.get('password',""))
        if user:
            auth.login(request, user)
            return redirect('/video/all/')

        else:
            return render(request, "sign.html")

    else:
        args["error"] = "The User exists already"
        return render(request, 'sign.html', args)

def hello(request):
	return HttpResponse("<h1>hello</h1>")
