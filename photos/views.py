from django.http import JsonResponse
from django.shortcuts import render
from PIL import Image
from .models import gallery
from .forms import UploadTempPhotosForm
from django.conf import settings
from utils import utils_image
import os

def upload_temp_photos(request):
    """
    View to handle uploading up to 10 temporary photos.
    """
    if request.method == 'POST':
        form = UploadTempPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            photos = request.FILES.getlist('photos') 

            if len(photos) > 10:
                form.add_error('photos', 
                               'You can upload a maximum of 10 photos.')
                return render(request, 
                              'photos/upload_temp_photos.html', {'form': form})
            
            image_paths = []
            tmp_dir = os.path.join(settings.MEDIA_ROOT, str(user_id), 'tmp')
            os.makedirs(tmp_dir, exist_ok=True)

            # Save each photo and record the path
            for photo in photos:
                new_image_name = utils_image.generate_image_name()
                temp_image_path = tmp_dir + '/' + new_image_name

                temp_image = Image.open(photo)
                temp_image.save(temp_image_path)
                image_paths.append(temp_image_path)
                temp_image.close()

            # Call Celery task
            # identify_clothes.delay(user_id, image_paths)

            print(image_paths)
            
            return JsonResponse({'status': 'Upload successful. Processing started.'})
    else:
        form = UploadTempPhotosForm()
    
    return render(request, 'photos/upload_temp_photos.html', {'form': form})
