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
        fields = ('no_of_artifact','bg_transparency','quiz_type','difficulty','font_name','font_size','font_color','bold','retention_period',
                  'file_share_path','bg_image_type','solid_color','bg_image')
        widgets = {
            'font_color': TextInput(attrs={'type': 'color','style':'padding:0px'}),
            'solid_color': TextInput(attrs={'type': 'color','style':'padding:0px'}),
        }


class UserDetailModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
