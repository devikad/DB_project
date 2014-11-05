from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from models import AppUser
from django import forms
from django.utils.html import strip_tags
from models import Comments
from django.db.models import Max


class UserCreateForm(UserCreationForm):
    # first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    # last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    # birthday = forms.DateField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Birth Date'}))
    # gender = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'gender'}))
    username = forms.EmailField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Email(username)'}))
    # phone_number = forms.IntegerField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Phone Number'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    def save(self, commit=True):
        maxid = AppUser.objects.all().aggregate(Max('user_id'))['user_id__max']
        if maxid == None:
            maxid = 1
        newuser = super(UserCreateForm, self).save(commit=False)
        # newuser = AppUser(username=self.cleaned_data['username'], email=self.cleaned_data['username'], user_id=(maxid+1) , lives_in_location=1)
        newuser.email = self.cleaned_data['username']
        newuser.user_id = maxid + 1
        newuser.lives_in_location = 1
        newuser.set_password(self.cleaned_data['password1'])
        if commit:
            newuser.save()
        return newuser

    class Meta:
        fields = ['username', 'password1', 'password2']
        model = AppUser


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form


class CommentsForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'class': 'commentsText'}))

    def is_valid(self):
        form = super(CommentsForm, self).is_valid()
        for f in self.errors.iterkeys():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error CommentsText'})
        return form

    class Meta:
        model = Comments
        exclude = ['comments_id']
