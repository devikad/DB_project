import re
import json
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
from forms import AuthenticateForm, UserCreateForm, CommentsForm
from models import UserGroup, AppUser, Location, AppUser1, University, Company, UniversityLocatedIn, CompanyLocatedIn, HasRelation, BelongsTo, StudiesIn, WorksIn
from django.db import connection
from models import *
from datetime import datetime
from django.db.models import Q


def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        user = request.user
        # first_name = user.profile.first_name
	location = Location.objects.get(location_id=user.lives_in_location)
        return render(request,
                      'userProfile.html',
                      {'first_name': user.username, 'location':location.name})
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
    return redirect('/groups/' + str(usergroup_id))


def usergroup_view(request, usergroup_id, comments_form=None):
    mbrship, loggedin = False, False
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
                      'next_url': '/groups/' + str(usergroup_id),
                  })

'''
The following function is never to be used again!
'''
def migrate(request):
    a = AppUser1.objects.all()
    #a = [allusers]
    #a.add(allusers)
    #print "got user", allusers.user_id
    #a = ['aa','bb','cc','dd','ee','ff','gg','hh','ii','jj','kk','ll','mm','nn','oo','pp','qq','rr','ss']
    for user in a:
	checkuser = AppUser.objects.filter(username=user.email)
	if checkuser.exists():
	    continue
	#em=user+'@'+user+'.com'
	newuser = super(UserCreateForm, self).save(commit=False)
        newuser = AppUser(username=em, email=em, lives_in_location=1, first_name=user, last_name=user)
        newuser.set_password(user)
        newuser.save()
	print "Inserted user",user
    return render(request, "migrate.html", {'msg':"success"})

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search_view(request):
    query_string = ''
    found_users, found_groups = None, None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        user_query = get_query(query_string, ['first_name', 'last_name', 'username'])
        group_query = get_query(query_string, ['name', 'about'])

        found_users = AppUser.objects.filter(user_query)
        found_groups = UserGroup.objects.filter(group_query)

    return render_to_response('search_form.html',
                          { 'query_string': query_string,
                            'found_users': found_users,
                            'found_groups': found_groups},
                          context_instance=RequestContext(request))

def profile(request, user_id):

    user = AppUser.objects.get(user_id=user_id)

    f1 = HasRelation.objects.filter(user_1_id=user_id)
    f2 = HasRelation.objects.filter(user_2_id=user_id)
    friends = []
    for f in f1:
	friend = AppUser.objects.get(user_id=f.user_2_id)
	friends.append(friend)
    for f in f2:
	friend = AppUser.objects.get(user_id=f.user_1_id)
        friends.append(friend)

    location = Location.objects.get(location_id=user.lives_in_location)
 
    comp = WorksIn.objects.filter(user_id=user_id)
    
    uni = StudiesIn.objects.filter(user_id=user_id)
     
    grp = BelongsTo.objects.filter(user_id=user_id)
    groups = []
    for g in grp:
	groups.append(g.group) 
    return render(request,
                  "userProfile.html",
                  {
                      'user': user,
                      'friends': friends,
                      'comp': comp,
                      'uni': uni,
                      'location': location,
                      'groups': groups,
                  })

def university(request, uni_id):
    uni = University.objects.get(university_id=uni_id)
    location = UniversityLocatedIn.objects.filter(university=uni_id)
    return render(request, "university.html", 
		  { 'uni': uni, 'location': location, }) 

def company(request, comp_id):
    comp = Company.objects.get(company_id=comp_id)
    location = CompanyLocatedIn.objects.filter(company=comp_id)
    return render(request, "company.html",
                  { 'comp': comp, 'location': location, })

def sn_graph_view(request, user_id):
    json_dict, nodes, links = dict(), list(), list()
    r1 = HasRelation.objects.filter(user_1_id=user_id)
    r2 = HasRelation.objects.filter(user_2_id=user_id)
    nodes.append({"name": AppUser.objects.get(user_id=user_id).username})  # source node
    for r in r1:
        nodes.append({"name": r.user_2.username})
    for r in r2:
        nodes.append({"name": r.user_1.username})
    for target_index in xrange(1, len(nodes)):
        links.append({"source":0, "target":target_index})
    json_dict["nodes"] = nodes
    json_dict["links"] = links
    json_data = json.dumps(json_dict)
    return render(request,
                  'sn_graph.html',
                    {
                        "json_data": json_data
                    })

