from user_profile.models import UserProfile,UserQuiz
from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import TextInput

User = get_user_model()


class UserProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'bio', 'location')


class UserQuizModelForm(forms.ModelForm):
    class Meta:
        model = UserQuiz
        fields = ('no_of_artifact','bg_transparency','quiz_type','difficulty','font_name','font_size','font_color','bold','retention_period'
                  ,'bg_image_type','solid_color','bg_image','tag_line_font_size','tag_line_text','local_folder','insrtctions','logo_image', 'test')
        widgets = {
            'no_of_artifact': TextInput(attrs={'type': 'number','min':'1'}),
            'bg_transparency': TextInput(attrs={'type': 'number','min':'1'}),
            'font_color': TextInput(attrs={'type': 'color','style':'padding:0px'}),
            'solid_color': TextInput(attrs={'type': 'color','style':'padding:0px'}),
        }
        labels = {
            'bg_transparency': "Background transparency",
            'retention_period': "Retention period (days)",
            'bg_image_type': "Background image type",
            'bg_image': "Background image",
            'tag_line_text': "Header",
            'tag_line_font_size': "Header Font Size",
            'insrtctions': "Instructions",
        }


class UserDetailModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
