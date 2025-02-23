import os
import json
import tempfile
from unittest.mock import patch
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth import authenticate


class UploadPhotosIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.upload_url = "/upload_photos/"
        self.user_id = "17"

        session = self.client.session
        session["client_id"] = self.user_id
        session.save()

        self.tmp_dir = os.path.join(settings.MEDIA_ROOT, self.user_id, "tmp")

    @patch("requests.post")
    def test_upload_images_success(self, mock_post):
        """Test uploading images successfully calls API"""
        
        mock_post.return_value.status_code = 200
        
        with open("photos/test/20240203_214331.jpg", "rb") as img_file:
            self.image_data = SimpleUploadedFile(
                name="20240203_214331.jpg",  
                content=img_file.read(),  
                content_type="image/jpeg"  
            )

        response = self.client.post(self.upload_url, {"photos": self.image_data}, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your images were uploaded successfully.")
        mock_post.assert_called_once()
        body = json.loads(mock_post.call_args[1]["data"])
        self.assertEqual(body["id"], self.user_id)
        self.assertEqual(len(body["images"]), 1)

    @patch("requests.post")
    def test_user_authentication(self, mock_post):
        response = self.client.post("/login/", {"email": "testuser@gmail.com","password": "TestUser@123"}, format="multipart")
        self.assertEqual(response.status_code, 200)
        
        mock_post.assert_not_called()
