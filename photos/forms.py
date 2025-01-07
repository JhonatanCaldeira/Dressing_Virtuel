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
    face_image = forms.ImageField(required=True, label='Face Image')

class SignUpForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, 
                               help_text="Enter a strong password")

    class Meta:
        model = ClientProfile
        fields = ['email', 'password']

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
        label="Usage Type"
    )
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(),
        required=False,
        label="Gender"
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        required=False,
        label="Season"
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        required=False,
        label="Color"
    )
    article_type = forms.ModelChoiceField(
        queryset=ArticleType.objects.all(),
        required=False,
        label="Article Type"
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
            self.fields['path'].label = "Current Image"
            image_path = (self.instance.path).replace('/home/jcaldeira/media/', settings.MEDIA_URL)
            self.fields['path'].help_text = mark_safe(
                f'<img src="{image_path}" alt="Image" style="max-width: 300px; max-height: 300px; border-radius: 8px;"/>'
        )