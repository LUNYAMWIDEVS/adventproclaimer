from django import forms
from froala_editor.widgets import FroalaEditor
from django.forms.widgets import HiddenInput
from messenger.tasks.whatsapp_manager import send_batch_whatsapp_text
from .models import Announcement, Assignment, Material
from messenger.models import Message

class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = True
        self.fields['description'].label = ''

    class Meta:
        model = Announcement
        fields = ['description']
        widgets = {
            'description': FroalaEditor(),
        }


class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label = ''
        self.fields['file'].required = False

    class Meta:
        model = Assignment
        fields = ('title', 'description', 'deadline', 'marks', 'file')
        widgets = {
            'description': FroalaEditor(),
            'title': forms.TextInput(attrs={'class': 'form-control mt-1', 'id': 'title', 'name': 'title', 'placeholder': 'Title'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control mt-1', 'id': 'deadline', 'name': 'deadline', 'type': 'datetime-local'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control mt-1', 'id': 'marks', 'name': 'marks', 'placeholder': 'Marks'}),
            'file': forms.TextInput(attrs={'class': 'form-control mt-1', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'placeholder': 'File'}),
        }


class MaterialForm(forms.ModelForm):
    book = forms.FileInput(attrs={'class': 'form-control', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'aria-label': 'Upload'})
    
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label = ""
        self.fields['file'].required = False
        self.fields['file'].widget = HiddenInput()


    class Meta:
        model = Material
        fields = ('description','file','pages')
        widgets = {
            'description': FroalaEditor(),
        }


class SplitMaterialsForm(forms.ModelForm):
    no_pages = forms.NumberInput(attrs={'class': 'form-control', 'id': 'no_pages', 'name': 'no_pages', 'placeholder': 'Number Of Pages'})

    def __init__(self, *args, **kwargs):
        super(SplitMaterialsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label=""
        self.fields['title'].required = False
        self.fields['title'].widget = HiddenInput()
    
    class Meta:
        model = Material
        fields = ('title',)

FORMATS = (
    ("N","---------"),
    ("E", "Email"),
    ("W", "Whatsapp"),
    ("P", "Phone Call"),
)
class ScheduleMaterialForm(forms.ModelForm):
    course_format = forms.ChoiceField(choices=FORMATS)
    minute = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'minute', 'name': 'minute', 'placeholder': 'Minute'}))
    hour = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'hour', 'name': 'hour', 'placeholder': 'Hour'}))

    class Meta:
        model = Message
        exclude = ('sent', 'message', 'recipient')
        widgets = {
            'course_format': forms.Select(attrs={'class': 'form-control'}),
        }