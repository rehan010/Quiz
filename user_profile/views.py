import textwrap
from string import ascii_letters
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect, reverse
from user_profile.forms import UserProfileModelForm, UserDetailModelForm,UserQuizModelForm
from fpdf import FPDF
from .models import UserQuiz
from PIL import Image, ImageDraw, ImageFont
from matplotlib import colors
from webcolors import name_to_rgb
import json
import numpy as np
import random
import textwrap


font_map={
        'Arial':'static/fonts/arial.ttf',
        'Helvetica':'static/fonts/helvetica.ttf',
        'Calibri':'static/fonts/calibri.ttf',
        'Futura':'static/fonts/futura.ttf',
        'Garamond':'static/fonts/garamond.ttf',
        'Times New Roman':'static/fonts/times new roman.ttf',
        'Cambria':'static/fonts/cambria.ttf',
        'Verdana':'static/fonts/verdana.ttf',
        'Rockwell':'static/fonts/rock.TTF',
        'Franklin Gothic':'static/fonts/Franklin gothic.ttf'
}

def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += str(ele) + " "
    # return string
    return str1

# def matrix_funct(df):
#     matrix=['2','3','5','?','6','7','8']
#     return listToString(matrix)


# sub functions

t = 0  # function return value, to be reset during each iteration
b = 3  # random parameter
n = 6  # random length of sequence
s = 2  # random sequential starting base value
q = 2  # calculated number of blank values to be filled with '?'


def f1(i):
    global t
    t = i + b*i*(i-2)
    return t


def f2(i):
    global t
    t = (i*i)+(t-b)
    return t


# main function - it returns matrix1

def matrix_funct(df):
    #matrix_funct(brave, difficulty):

    b = random.randint(1, 4)
    n = random.randint(6, 12)
    s = random.randint(1, 3)

    # q:('?'): n<7:1 n<9:2 n<11:3 n<13:4

    if n < 7:
        q = 1
    elif n < 9:
        q = 2
    elif n < 11:
        q = 3
    elif n < 13:
        q = 4
    else:
        q = 1


    #print(f' b:{b} n:{n} s:{s} q:{q}')

    matrix1 = list(map(f1, range(s, n+s)))
    matrix1.append('?')

    m1idx = random.sample(range(0, n-2), q)
    dic = {}
    for i in range(len(m1idx)):
        dic[m1idx[i]] = '?'

    for index, item in enumerate(matrix1):
        for i in m1idx:
            matrix1[i] = dic[i]

    t = 0
    matrix2 = list(map(f1, range(s, n + s+1)))

    #print(f'Quiz: {matrix1}')
    #print(f'Answer: {matrix2}')

    return listToString(matrix1)


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
            f = font_map[UserQuiz.FONT_CHOICES[int(request.POST['font_name']) - 1][1]]

            if obj.test == True:

                tag_line_text= str(obj.tag_line_text)
                tag_line_text_lines= textwrap.wrap(str(obj.tag_line_text), width=30)
                matrix_text= str(matrix_funct(obj))
                matrix_text_lines= textwrap.wrap(str(matrix_funct(obj)), width=15)

                W, H = (1200, 1200)
                font = ImageFont.truetype(f, size=int(request.POST['font_size']))
                tag_font = ImageFont.truetype(f, size=int(request.POST['tag_line_font_size']))
                if request.POST['bg_image_type'] == 's':
                    img = Image.new('RGB', (W, H), obj.solid_color)

                else:
                    img = Image.open(request.FILES['bg_image'])
                    newsize = (1200, 1200)
                    img = img.resize(newsize)
                d = ImageDraw.Draw(img)
                font_width, font_height = d.textsize( matrix_text,font=font)
                new_width = (img.size[0] - font_width) / 2
                new_height = (img.size[1] - font_height) / 2
                #
                w, h = d.textsize(tag_line_text,font=tag_font)
                # tag_width = (img.size[0] - w) /2
                tag_height = (img.size[1] - h) / 8

                MAX_W= img.size[0]
                current_h, pad = tag_height, 10
                for line in tag_line_text_lines:
                    w, h = d.textsize(line, font=font)
                    d.text(((MAX_W - w) / 2, current_h), line, font=font, fill=obj.font_color,anchor="mm")
                    current_h += h + pad


                # d.text(xy=(tag_width, tag_height), text=tag_line_text, font=tag_font, fill=obj.font_color,
                #        anchor="mm")
                d.text(xy=(new_width, new_height), text=matrix_text, font=font, fill=obj.font_color,
                       anchor="mm")
                img.save('media/test/' + 'test' + '.png')
                response = {'image_url': '/media/test/test.png','status':1}

                return HttpResponse(json.dumps(response),content_type='application/json')


            else:
                obj.user = self.request.user

                obj.save()
                matrix_funct(obj)
                W, H = (1200, 1200)
                font = ImageFont.truetype(f, size=int(request.POST['font_size']))
                tag_font = ImageFont.truetype(f, size=int(request.POST['tag_line_font_size']))
                if request.POST['bg_image_type'] == 's':
                    img = Image.new('RGB', (W, H), obj.solid_color)

                else:
                    img = Image.open(request.FILES['bg_image'])
                    newsize = (1200, 1200)
                    img = img.resize(newsize)
                d = ImageDraw.Draw(img)
                font_width, font_height = font.getsize(str(matrix_funct(d)))
                new_width = (img.size[0] - font_width) / 2
                new_height = (img.size[1] - font_height * 0.21) / 2

                w, h = d.textsize(str(obj.tag_line_text), font=tag_font)
                tag_width = (img.size[0] - w) / 2
                tag_height = (img.size[1] - h) / 8

                d.text(xy=(tag_width, tag_height), text=str(obj.tag_line_text), font=tag_font, fill=obj.font_color,
                       anchor="mm")
                d.text(xy=(new_width, new_height), text=str(matrix_funct(d)), font=font, fill=obj.font_color,
                       anchor="mm")
                img.save('media/img/'+obj.artifact_name+'.png')

                return redirect(reverse('quiz'))
        else:
            print(user_quiz_form.errors, "++++++")

        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        context = super(UserQuizView, self).get_context_data(**kwargs)

        context['user_quiz_form'] = UserQuizModelForm()
        return render(request, self.template_name, context=context)

