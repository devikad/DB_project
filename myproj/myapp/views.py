import re
import json
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
from forms import AuthenticateForm, UserCreateForm, CommentsForm, CreateGroupForm
from django.db import connection
from models import *
from datetime import datetime
from django.db.models import Q


def index(request, form_valid=True, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        user = request.user
        return redirect('/profile/'+str(user.user_id))
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                      'login_signup.html',
                      {'form_valid': form_valid,
                       'auth_form': auth_form,
                       'user_form': user_form, })


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
            password1 = user_form.cleaned_data.get('password1')
            password2 = user_form.cleaned_data.get('password2')
            if password1 == password2:
                user_form.save()
                user = authenticate(username=username, password=password2)
                login(request, user)
                return redirect('/')
        return index(request, form_valid=False, user_form=user_form)
    return redirect('/')


def submit_comments(request):
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
            return redirect(next_url)
        else:
            return redirect('/')
    return redirect('/')


def create_group_view(request):
    if request.user.is_authenticated():
        group_form = CreateGroupForm()
        return render(request, 'creategroup.html',
                      {
                          'group_form': group_form
                      })
    return redirect('/')


def create_group_submit(request):
    group_form = CreateGroupForm(data=request.POST)
    if request.method == 'POST':
        if group_form.is_valid():
            newgroup = group_form.save(commit=False)
            newgroup.admin = request.user
            newgroup.save()
            BelongsTo(user=request.user,
                      group=newgroup).save()
            return redirect('/groups/' + str(newgroup.usergroup_id))
    return redirect('/create_group_view')


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
    found_users, found_groups, found_companies, found_universities = None, None, None, None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        user_query = get_query(query_string, ['first_name', 'last_name'])
        group_query = get_query(query_string, ['name'])
        company_query = get_query(query_string, ['name'])
        university_query = get_query(query_string, ['name'])

        found_users = AppUser.objects.filter(user_query)
        found_groups = UserGroup.objects.filter(group_query)
        found_companies = Company.objects.filter(company_query)
        found_universities = University.objects.filter(university_query)

    return render_to_response('search_form.html',
                              {'query_string': query_string,
                               'found_users': found_users,
                               'found_groups': found_groups,
                               'found_companies': found_companies,
                               'found_universities': found_universities},
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

    intr = HasInterest.objects.filter(user_id=user_id)
    try:
        location = Location.objects.get(location_id=user.lives_in_location_id)
    except:
        location = ''
    comp = WorksIn.objects.filter(user_id=user_id)

    uni = StudiesIn.objects.filter(user_id=user_id)

    grp = BelongsTo.objects.filter(user_id=user_id)
    groups = []
    for g in grp:
        groups.append(g.group)

    grps = group_reco(user_id)
    greco = []
    for g in grps:
        fetch_g = UserGroup.objects.get(name=g[0])
        greco.append(fetch_g)

    frns = friend_reco(user_id)
    freco = []
    for f in frns:
        fetch_f = AppUser.objects.get(user_id=int(f[0]))
        freco.append(fetch_f)

    return render(request,
                  "userProfile.html",
                  {
                      'user': user,
                      'friends': friends,
                      'comp': comp,
                      'uni': uni,
                      'location': location,
                      'groups': groups,
                      'greco': greco,
                      'freco': freco,
                      'intr': intr,
                  })


def friend_reco(user_id):
    cursor = connection.cursor()
    sql = '''select *
from
(
  select i2.user_id,count(i2.user_id) as no_of_common_friends
  from HAS_INTEREST i, HAS_INTEREST i2,
        (
          (
            select i2.user_id
            from studies_in i1, studies_in i2
            where i1.university_id = i2.university_id and
              i1.user_id = ''' + str(user_id) + ''' and i2.user_id <> ''' + str(user_id) + '''
          )
          minus
          (
            select r.USER_2_ID
            from has_relation r
            where user_1_id=''' + str(user_id) + '''
            union
            select r2.USER_1_ID
            from has_relation r2
            where user_2_id=''' + str(user_id) + '''
          )
        ) same_univ
  where i.INTEREST_ID = i2.INTEREST_ID and
        same_univ.user_id = i2.USER_ID and
        i.user_id = ''' + str(user_id) + ''' and i2.user_id<>''' + str(user_id) + '''
  group by i2.user_id
  order by count(i2.user_id) desc
)
where rownum<6;'''
    cursor.execute(sql)
    return cursor


def group_reco(user_id):
    cursor = connection.cursor()
    sql = '''select name as Interest_name, no_of_friends_in_grp
from user_group,
(
  select *
  from
  (
        select group_id, count(user_id) As no_of_friends_in_grp
        from belongs_to
        where belongs_to.user_id in
        (
          (    
            SELECT User_2_id
            FROM has_relation
            WHERE user_1_id = ''' + str(user_id) + '''
          )
          UNION
          (
            SELECT User_1_id
            FROM has_relation
            WHERE user_2_id = ''' + str(user_id) + '''
          )
        )
        group by(group_id)
  )
  where group_id
  not in
  (
        select group_id
        from belongs_to
        where user_id=''' + str(user_id) + '''
  )
  order by no_of_friends_in_grp desc
) tmp
where tmp.group_id = user_group.USERGROUP_ID;'''
    cursor.execute(sql)
    return cursor


def university(request, uni_id):
    uni = University.objects.get(university_id=uni_id)
    location = UniversityLocatedIn.objects.filter(university=uni_id)
    return render(request, "university.html",
                  {'uni': uni, 'location': location, })


def company(request, comp_id):
    comp = Company.objects.get(company_id=comp_id)
    location = CompanyLocatedIn.objects.filter(company=comp_id)
    return render(request, "company.html",
                  {'comp': comp, 'location': location, })


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
        links.append({"source": 0, "target": target_index})
    json_dict["nodes"] = nodes
    json_dict["links"] = links
    json_data = json.dumps(json_dict)
    return render(request,
                  'sn_graph.html',
                  {
                      "json_data": json_data
                  })