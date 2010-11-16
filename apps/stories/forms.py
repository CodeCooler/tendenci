import imghdr
from os.path import splitext
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from stories.models import Story
from perms.forms import TendenciBaseForm
from perms.utils import is_admin
from base.fields import SplitDateTimeField

ALLOWED_LOGO_EXT = (
    '.jpg',
    '.jpeg',
    '.gif',
    '.png' 
)   

class StoryForm(TendenciBaseForm):
    fullstorylink = forms.CharField(label=_("Full Story Link"), required=False, max_length=300)
    start_dt = SplitDateTimeField(label=_('Start Date/Time'), initial=datetime.now())
    end_dt = SplitDateTimeField(label=_('End Date/Time'), initial=datetime.now())

    status_detail = forms.ChoiceField(
        choices=(('active','Active'),('inactive','Inactive'), ('pending','Pending'),))

    class Meta:
        model = Story

        fields = (
            'title',
            'content',
            'photo',
            'full_story_link',
            'tags',
            'start_dt',
            'end_dt',
            'syndicate',
            'allow_anonymous_view',
            'user_perms',
            'group_perms',
            'status',
            'status_detail',
        )

        fieldsets = [('Story Information', {
                      'fields': ['title',
                                 'content',
                                 'photo',
                                 'full_story_link',
                                 'tags',
                                 'start_dt',
                                 'end_dt',
                                 ],
                      'legend': ''
                      }),
                      ('Permissions', {
                      'fields': ['allow_anonymous_view',
                                 'user_perms',
                                 'group_perms',
                                 ],
                      'classes': ['permissions'],
                      }),
                     ('Administrator Only', {
                      'fields': ['syndicate',
                                 'status',
                                 'status_detail'], 
                      'classes': ['admin-only'],
                    })]   

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            extension = splitext(photo.name)[1]
            
            # check the extension
            if extension.lower() not in ALLOWED_LOGO_EXT:
                raise forms.ValidationError('The photo must be of jpg, gif, or png image type.')
            
            # check the image header
            image_type = '.%s' % imghdr.what('', photo.read())
            if image_type not in ALLOWED_LOGO_EXT:
                raise forms.ValidationError('The photo is an invalid image. Try uploading another photo.')

        return photo
                 
    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        if not is_admin(self.user):
            if 'status' in self.fields: self.fields.pop('status')
            if 'status_detail' in self.fields: self.fields.pop('status_detail')

      
class UploadStoryImageForm(forms.Form):
    file  = forms.FileField(label=_("File Path"))


