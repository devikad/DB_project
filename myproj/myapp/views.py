from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from forms import AuthenticateForm, UserCreateForm, CommentsForm
from models import *
from datetime import datetime


def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        user = request.user
        # first_name = user.profile.first_name
        return render(request,
                      'userProfile.html',
                      {'first_name': user.username})
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
        group_id = next_url.split("/")[2]
        if comments_form.is_valid():
            comment = comments_form.save()
            MakeComment(posting_time=datetime.now(),
                        group=UserGroup.objects.get(usergroup_id=group_id),
                        user=request.user,
                        comment=comment).save()
            print "commentrs_form is valid!"
            print "next_url:", next_url
            return redirect(next_url)
        else:
            print "comments_form is not valid!"
            return redirect('/')
    print "request type is not POST!"
    return redirect('/')


def join_group(request, usergroup_id):
    print "joinning group..."
    BelongsTo(user=request.user,
              group=UserGroup.objects.get(usergroup_id=usergroup_id)).save()
    return redirect('/groups/'+str(usergroup_id))


def usergroup_view(request, usergroup_id, comments_form=None):
    mbrship,loggedin = False, False
    usergroup = UserGroup.objects.get(usergroup_id=usergroup_id)
    if request.user.is_authenticated():  # User is logged in
        user = request.user
        loggedin = True
        group_mbrs = [b_relation.user for b_relation in usergroup.belongsto_set.all()]
        if user in group_mbrs:  # current user belongs to the group
            mbrship = True
    comments_form = comments_form or CommentsForm()
    comments = [i.comment for i in usergroup.makecomment_set.all()]
    return render(request,
                  "base_groups.html",
                  {
                      'comments_form': comments_form,
                      'usergroup': usergroup,
                      'comments': comments,
                      'mbrship': mbrship,
                      'loggedin': loggedin,
                      'next_url': '/groups/'+str(usergroup_id),
                  })
