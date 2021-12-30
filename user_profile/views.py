from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect, reverse
from user_profile.forms import UserProfileModelForm, UserDetailModelForm,UserQuizModelForm
from fpdf import FPDF
from .models import UserQuiz
from PIL import Image, ImageDraw
from matplotlib import colors
import numpy as np
from webcolors import name_to_rgb
def matrix_funct(df):
    matrix=[['2','3','5','?']]
    return matrix



class UserProfileView(TemplateView, LoginRequiredMixin):
    template_name = "user_profile/profile.html"

    def post(self, request, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['user_profile_form'] = user_profile_form = UserProfileModelForm(request.POST, request.FILES,
                                                                                instance=request.user.user_profile)
        context['user_detail_form'] = user_detail_form = UserDetailModelForm(request.POST,
                                                                             instance=request.user)
        if user_profile_form.is_valid() and user_detail_form.is_valid():
            user_profile_form.save()
            user_detail_form.save()
            return redirect(reverse('profile'))
        else:
            print(user_profile_form.errors, "++++++")

        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['user_profile_form'] = UserProfileModelForm(instance=request.user.user_profile)
        context['user_detail_form'] = UserDetailModelForm(instance=request.user)
        return render(request, self.template_name, context=context)


class UserStatusView(TemplateView, LoginRequiredMixin):
    template_name = "user_profile/status.html"


class UserQuizView(TemplateView, LoginRequiredMixin):
    template_name = "user_profile/quiz.html"

    def post(self, request, *args, **kwargs):
        context = super(UserQuizView, self).get_context_data(**kwargs)

        context['user_quiz_form'] = user_quiz_form = UserQuizModelForm(request.POST, request.FILES)

        if user_quiz_form.is_valid() :

            obj = user_quiz_form.save(commit=False)
            obj.user = self.request.user
            # we can call our matrix function here we can access all params here

            obj.save()
            matrix_funct(obj)

            img = Image.new('RGB', (300, 200),name_to_rgb(obj.solid_color, spec='css3'))
            # img.putalpha(255)
            d = ImageDraw.Draw(img)
            d.text((10, 10), str(matrix_funct(d)), fill=name_to_rgb(obj.font_color, spec='css3'))
            img.save('media/img/'+obj.artifact_name+'.png')




            # w, h = 512, 512
            # data = np.zeros((h, w, 3), dtype=np.uint8)
            # data[0:256, 0:256] = [255, 0, 0]  # red patch in upper left
            # img = Image.fromarray(data, 'RGB')
            # img.save('my.png')
            # from PIL import Image, ImageDraw
            #
            # img = Image.new('RGB', (100, 30), color=(73, 109, 137))
            #
            # d = ImageDraw.Draw(img)
            # d.text((10, 10), "Hello World", fill=(255, 255, 0))
            #
            # img.save('media/img/'+obj.artifact_name+'.png')
            # pdf = FPDF()
            # pdf.add_page()
            # pdf.set_font(UserQuiz.FONT_CHOICES[int(obj.font_name)-1][1], 'B', obj.font_size)
            # pdf.cell(40, 10, "User with ID "+str(obj.user.pk) + " created with filename " + obj.artifact_name)
            # pdf.output('media/pdf/' + obj.artifact_name + '.pdf', 'F')

            return redirect(reverse('quiz'))
        else:
            print(user_quiz_form.errors, "++++++")

        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        context = super(UserQuizView, self).get_context_data(**kwargs)

        context['user_quiz_form'] = UserQuizModelForm()
        return render(request, self.template_name, context=context)

