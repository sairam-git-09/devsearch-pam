from django.forms import ModelForm
from .models import Profile, Skill, Message 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',  
            'email': 'Email Address',
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image', 'social_github', 'social_twitter', 'social_linkedin', 'social_youtube', 'social_website']
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})
            
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})
            
            
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})