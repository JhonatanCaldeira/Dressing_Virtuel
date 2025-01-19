from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.conf import settings

from django.contrib.auth.password_validation import validate_password
from .models import (
    ClientProfile,
    ImageProduct, 
    ArticleType,
    ProductSubCategory,
    ProductCategory,
    Season,
    Color,
    Gender,
    UsageType
)

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'class': 'form-control'})
        super().__init__(*args, **kwargs)

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class FileFieldForm(forms.Form):
    file_field = MultipleFileField()

class UploadTempPhotosForm(forms.Form):
    """
    Form for uploading up to 10 temporary photos.
    """
    photos = MultipleFileField()

class UploadFaceImageForm(forms.Form):
    """
    Form for uploading a single face image.
    """
    face_image = forms.ImageField(required=True, 
                                  label='Face Image',
                                  widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class SignUpForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        help_text="Password must have at least 9 characters, including at least one special character from !@#$%^&*()_+"
    )

    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'You must accept the terms to register.'}
    )

    class Meta:
        model = ClientProfile
        fields = ['email', 'password', 'accept_terms']
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 
                                             'placeholder': 'Enter your email'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)  
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password  


class EditImageProductForm(forms.ModelForm):
    """
    Form to edit an ImageProduct instance.
    """
    usage_type = forms.ModelChoiceField(
        queryset=UsageType.objects.all(),
        required=False,
        label="Usage",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(),
        required=False,
        label="Gender",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        required=False,
        label="Season",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        required=False,
        label="Color",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    article_type = forms.ModelChoiceField(
        queryset=ArticleType.objects.all(),
        required=False,
        label="Article",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    client = forms.HiddenInput()

    class Meta:
        model = ImageProduct
        fields = ['path', 'usage_type', 'gender', 'season', 'color', 'article_type']
        widgets = {
            'path': forms.TextInput(attrs={'readonly': 'readonly', 'style': 'display:none;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Set initial choices or ordering for fields
        self.fields['usage_type'].queryset = UsageType.objects.order_by('name')
        self.fields['gender'].queryset = Gender.objects.order_by('gender')
        self.fields['season'].queryset = Season.objects.order_by('name')
        self.fields['color'].queryset = Color.objects.order_by('name')
        self.fields['article_type'].queryset = ArticleType.objects.order_by('name')

        if self.instance and self.instance.path:
            self.fields['path'].label = ""
            image_path = (self.instance.path).replace('/home/jcaldeira/media/', settings.MEDIA_URL)
            self.fields['path'].help_text = mark_safe(
                f'<img src="{image_path}" alt="Image" style="max-width: 300px; max-height: 300px; border-radius: 8px;"/>'
        )