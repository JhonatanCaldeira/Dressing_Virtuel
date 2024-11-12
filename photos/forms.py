from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import ClientProfile

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
    