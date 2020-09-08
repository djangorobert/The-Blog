from django import forms
from .models import Post, Comment
from django.contrib.auth import authenticate, get_user_model



User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('__all__')

class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'rows': 4
    }))
    class Meta:
        model = Comment
        fields = ('content',)

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('The username or password was incorrect')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2'
        ]

    def clean(self, *args, **kwargs):
            
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2:
            if password != password2:
                raise forms.ValidationError('The Passwords do not match')
            
        return super(UserRegisterForm, self).clean(*args, **kwargs)