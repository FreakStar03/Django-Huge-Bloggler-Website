# import form class from django 
from django import forms   
# import GeeksModel from models.py 
from .models import Post , Comment

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
  
# create a ModelForm 
class Post_form(forms.ModelForm): 
    # specify the name of model to use 
    class Meta: 
        model = Post
        widgets = {
        'content': SummernoteWidget(),
        }
        fields =  "__all__"

        exclude = ['author' , 'status' , 'slug']

# class comments_form(forms.ModelForm): 
#     # specify the name of model to use
#     class Meta:
#         model = Comment
#         fields = ('author', 'text',)
#     # class Meta: 
#     #     model = Comment 
#     #     fields = "__all__"
#     def save(self):
#     	user_profile = super(comments_form , self).save(commit=False) 
#     	user_profile.save()


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email' , 'password1' , 'password2']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')





