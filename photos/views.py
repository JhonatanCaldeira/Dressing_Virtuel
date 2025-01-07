from django.http import JsonResponse
from PIL import Image, ExifTags
from .models import ClientProfile, ImageProduct
from .forms import (UploadTempPhotosForm,
                    SignUpForm,
                    UploadFaceImageForm,
                    EditImageProductForm)
from django.conf import settings
from utils import utils_image
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
import base64
import requests
import json
import os
import imghdr

CELERY_API_SERVER = os.getenv("CELERY_API_SERVER")
CELERY_API_PORT = os.getenv("CELERY_API_PORT")
CELERY_API_ENDPONT = os.getenv("CELERY_API_ENDPONT")

CELERY_API = f"http://{CELERY_API_SERVER}:{CELERY_API_PORT}/{CELERY_API_ENDPONT}"
CELERY_API_KEY = os.getenv("CELERY_API_KEY")

DB_API_SERVER = os.getenv("PG_API_SERVER")
DB_API_PORT = os.getenv("PG_API_PORT")
DB_API_ENDPONT = os.getenv("PG_API_ENDPONT")

DB_API = f"http://{DB_API_SERVER}:{DB_API_PORT}/{DB_API_ENDPONT}"
DB_API_KEY = os.getenv("PG_API_KEY")


def main_view(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login_view') 
    else:
        form = SignUpForm()
    return render(request, 'create_user.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            request.session['client_id'] = user.id
            return redirect('main_view') 
        else:
            return HttpResponse("Invalid email or password", status=401)
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login_view')

def upload_faceid(request):
    user_id = request.session.get('client_id')
    client = ClientProfile.objects.get(id=user_id)
    existing_face_id = None

    if client.face_id:
        image_data = base64.b64decode(client.face_id)
        mime_type = imghdr.what(None, h=image_data) or "jpeg" 
        face_id_b64_str = client.face_id.tobytes().decode('utf-8')
        existing_face_id = f"data:image/{mime_type};charset=utf-8;base64,{face_id_b64_str}"

    if request.method == 'POST':
        form = UploadFaceImageForm(request.POST, request.FILES)
        if form.is_valid():
            face_image = form.cleaned_data['face_image']
            image_content = face_image.read()
            face_id_base64 = base64.b64encode(image_content).decode('utf-8')

            client.update_face_id(face_id_base64)

            return redirect('upload_faceid') 
    else:
        form = UploadFaceImageForm()

    return render(request, 'upload_faceid.html', 
                  {'form': form, 'existing_face_id': existing_face_id})



def upload_photos(request):
    """
    View to handle uploading up to 10 temporary photos.
    """
    if request.method == 'POST':
        form = UploadTempPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session.get('client_id')
            photos = request.FILES.getlist('photos') 

            if len(photos) > 10:
                form.add_error('photos', 
                               'You can upload a maximum of 10 photos.')
                return render(request, 
                              'upload_temp_photos.html', {'form': form})
            
            image_paths = []
            tmp_dir = os.path.join(settings.MEDIA_ROOT, str(user_id), 'tmp')
            os.makedirs(tmp_dir, exist_ok=True)

            # Save each photo and record the path
            for photo in photos:
                new_image_name = utils_image.generate_image_name()
                temp_image_path = os.path.join(tmp_dir, new_image_name)

                temp_image = Image.open(photo)

                # Adjust orientation based on EXIF data
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    exif = temp_image._getexif()
                    if exif is not None:
                        orientation = exif.get(orientation, None)
                        if orientation == 3:
                            temp_image = temp_image.rotate(180, expand=True)
                        elif orientation == 6:
                            temp_image = temp_image.rotate(270, expand=True)
                        elif orientation == 8:
                            temp_image = temp_image.rotate(90, expand=True)
                except (AttributeError, KeyError, IndexError):
                    # No EXIF data or error processing it
                    pass

                temp_image.save(temp_image_path)
                image_paths.append(temp_image_path)
                temp_image.close()

            # Call Celery task
            header={"access_token":CELERY_API_KEY}
            body={"id":user_id,"images":image_paths}

            response = requests.post(f"{CELERY_API}/task_image_classification",
                                data=json.dumps(body),
                                headers=header)
            
            response =  response.json()
            print(image_paths)

            return JsonResponse({'status': 'Upload successful. Processing started.'})
    else:
        form = UploadTempPhotosForm()
    
    return render(request, 'upload_photos.html', {'form': form})

def show_images_from_user_old(request):
    if request.method == 'GET':
        user_id = request.session.get('client_id')

        header={"access_token":DB_API_KEY}
        body={"id":user_id}

        response = requests.get(f"{DB_API}/images_from_client/?client_id={user_id}",
                            headers=header)
        
        articles = json.loads(response.text)
        for article in articles:
            article['path'] = article['path'].replace('/home/jcaldeira/media/', settings.MEDIA_URL)

        return render(request, 'list_of_clothes.html', {'clothes': articles})
    else:
        return redirect('upload_photos')
    
def delete_multiple_clothes(request):
    user_id = request.session.get('client_id')

    if not user_id:
        return redirect('login_view')
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_clothes') 
        if selected_ids:
            ImageProduct.objects.filter(id__in=selected_ids).delete()
            messages.success(request, "Selected images have been deleted.")
            return redirect('list_of_clothes')
    else:
        return redirect('list_of_clothes')

   
def show_images_from_user(request):
    if request.method == 'GET':
        user_id = request.session.get('client_id')

        if not user_id:
            return redirect('login_view')

        query = request.GET.get('query', '').strip()
        clothes_data = []
        clothes = ImageProduct.objects.filter(client_id=user_id)

        if query:
            clothes = clothes.filter(
                            Q(article_type__name__icontains=query) |
                            Q(color__name__icontains=query) |
                            Q(gender__gender__icontains=query) |
                            Q(season__name__icontains=query) |
                            Q(usage_type__name__icontains=query)
                        )
        else:
            clothes = clothes.select_related(
                'article_type', 'color', 'gender', 'season', 'usage_type'
            )

        for item in clothes:
            clothes_data.append({
                'id': item.id,
                'path': item.path.replace('/home/jcaldeira/media/', settings.MEDIA_URL) if item.path else None,
                'name': item.article_type.name if item.article_type else "No Article",
                'article': item.article_type.name if item.article_type else None,
            })

        return render(request, 'list_of_clothes.html', {'clothes': clothes_data})
    else:
        return redirect('upload_photos')            

def edit_image_product(request, image_product_id):
    """
    View to edit an existing ImageProduct.
    """
    user_id = request.session.get('client_id')

    if not user_id:
        return redirect('login_view')

    image_product = get_object_or_404(ImageProduct, id=image_product_id)

    if request.method == 'POST':
        form = EditImageProductForm(request.POST, instance=image_product)
        if form.is_valid():
            form.save()  
    else:
        form = EditImageProductForm(instance=image_product) 
    return render(request, 'edit_image_product.html', {'form': form})