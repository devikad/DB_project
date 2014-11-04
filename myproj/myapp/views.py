from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from forms import AuthenticateForm, UserCreateForm, CommentsForm
from models import UserGroup
from django.db import connection


def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        user = request.user
        # first_name = user.profile.first_name
        return render(request,
                      'userProfile.html',
                      {'first_name': user.id})
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                      'login_signup.html',
                      {'auth_form': auth_form, 'user_form': user_form, })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')


def submit_comments(request):
    print "submitting comments..."
    if request.method == "POST":
        comments_form = CommentsForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if comments_form.is_valid():
            comments_form.save()
            # user_id = request.user.user_id
            # group_id =
            # cursor = connection.cursor()
            # cursor.execute('''INSERT INTO make_comment () values()''')
            print "comments_form is valid!"
            return redirect(next_url)
        else:
            print "comments_form is not valid!"
            return redirect('/')
    print "request type is not POST!"
    return redirect('/')


def usergroup_view(request, usergroup_id, comments_form=None):
    usergroup = UserGroup.objects.get(usergroup_id=usergroup_id)
    comments_form = comments_form or CommentsForm()
    comments = [i.comment for i in usergroup.makecomment_set.all()]
    return render(request,
                  "base_groups.html",
                  {
                      'comments_form': comments_form,
                      'usergroup': usergroup,
                      'comments': comments,
                  })