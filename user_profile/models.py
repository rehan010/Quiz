from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import BytesIO
import logging
from django.core.files.base import ContentFile
from placeholder_pics.placeholder import PlaceholderPic
from django_thumbs.fields import ImageThumbsField
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from django.utils import timezone
import datetime

logger = logging.getLogger(__name__)


# Create your models here.
def upload_avatar_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'userprofile/%s%s' % (
        timezone.now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )


class UserProfile(models.Model):
    SIZES = (
        {'code': '60x60', 'wxh': '60x60', 'resize': 'crop'},  #
        {'code': '100x100', 'wxh': '100x100', 'resize': 'crop'},
        {'code': '200x200', 'wxh': '200x200', 'resize': 'crop'},  # 'resize' defaults to 'scale'
        {'code': '400x400', 'wxh': '400x400', 'resize': 'crop'},  # 'resize' defaults to 'scale'
    )

    THUMBNAIL_ALIASES = {
        '': {
            'avatar': {'size': (50, 50), 'crop': True},
        },
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    image = ImageThumbsField(default=None, verbose_name="profile image",
                             sizes=SIZES,
                             upload_to=upload_avatar_to, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, default=None, verbose_name="Write about your self")
    location = models.CharField(max_length=30, blank=True, null=True, default=None)
    birth_date = models.DateField(null=True, blank=True)

    def generate_img(self):
        f = BytesIO()
        logger.debug("generating image")
        if self.user.first_name:
            img_name = self.user.first_name[:2].capitalize()
        else:
            img_name = self.user.email[:2].capitalize()
        placeholder = PlaceholderPic(img_name)
        placeholder.image.save(f, format='png')
        s = f.getvalue()

        self.image.save("%s.png" % self.user.id,
                        ContentFile(s))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        if not profile.image:
            profile.generate_img()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()


class UserQuiz(models.Model):
    QUIZ_CHOICES = (
        ('s', 'Sequential'),
        ('p', 'Progression'),
    )
    DIFFICULTY_CHOICES = (
        ('g', 'Green'),
        ('b', 'Blue'),
        ('r', 'Red'),
    )
    BG_IMAGE_CHOICES = (
        ('s', 'Solid'),
        ('i', 'Image'),
    )
    FONT_CHOICES = (
        ('1', 'Arial'),
        ('2', 'Helvetica'),
        ('3', 'Calibri'),
        ('4', 'Futura'),
        ('5', 'Garamond'),
        ('6', 'Times New Roman'),
        ('7', 'Cambria'),
        ('8', 'Verdana'),
        ('9', 'Rockwell'),
        ('10', 'Franklin Gothic'),
    )
    BOOL_CHOICES = ((True, 'Y'), (False, 'N'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_quiz")
    no_of_artifact = models.IntegerField(default=1, validators=[MaxValueValidator(100),MinValueValidator(1)], blank=True, null=True)
    bg_transparency = models.IntegerField(default=1, validators=[MaxValueValidator(100),MinValueValidator(1)], blank=True, null=True)
    artifact_name= models.CharField(editable=False,max_length=30)
    quiz_type = models.CharField(max_length=20, null=True, choices=QUIZ_CHOICES,default='s')
    difficulty = models.CharField(max_length=20, null=True, choices=DIFFICULTY_CHOICES,default='b')
    font_name = models.CharField(max_length=20, null=True, choices=FONT_CHOICES,default='1')
    font_size = models.IntegerField(default=25,null=True,blank=True)
    font_color = models.CharField(max_length=20,default="White")
    bold = models.BooleanField(choices=BOOL_CHOICES,default=False)
    retention_period = models.IntegerField(default=270,null=True,blank=True)
    file_share_path = models.CharField(max_length=100, default="https://")
    bg_image_type = models.CharField(max_length=20, null=True, choices=BG_IMAGE_CHOICES,default='s')
    solid_color = models.CharField(max_length=50,null=True,blank=True, default="Blue")
    bg_image = models.ImageField(null=True,blank=True,default="https://www.w3schools.com/images/picture.jpg")


    def getImage(self):
        if not self.image:
            # depending on your template
            return "https://www.w3schools.com/images/picture.jpg"



    def save(self, *args, **kwargs):
        current_version = UserQuiz.objects.all().last()
        quiz_type=self.quiz_type


        if current_version:
            version=int(current_version.artifact_name.split("_")[1][:-1])
            date=str(current_version.artifact_name.split("_")[0])

            if date == str(datetime.date.today()):
                    version=str(version+1)
                    self.artifact_name = str(datetime.date.today()) + "_" + version +quiz_type

            else:
                self.artifact_name = str(datetime.date.today()) + "_" + str(1)+quiz_type
        else:
            self.artifact_name = str(datetime.date.today())+"_"+ str(1)+quiz_type
        super(UserQuiz, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.artifact_name)
