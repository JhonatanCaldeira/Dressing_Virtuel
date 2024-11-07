from django import forms

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
    user_id = forms.CharField(max_length=100, label='User ID')
    photos = MultipleFileField()

class UploadFaceImageForm(forms.Form):
    """
    Form for uploading a single face image.
    """
    user_id = forms.CharField(max_length=100, label='User ID')
    face_image = forms.ImageField(required=True, label='Face Image')
