from django.contrib import admin
from user_profile.models import UserProfile,UserQuiz

# Register your models here.

class QuizInline(admin.ModelAdmin):
    list_display = ('user','artifact_name','no_of_artifact','bg_transparency','quiz_type','difficulty','font_name','font_size','font_color','bold','retention_period',
                  'bg_image_type','solid_color','bg_image')
    search_fields = ('artifact_name',)

admin.site.register(UserProfile)
admin.site.register(UserQuiz,QuizInline)
