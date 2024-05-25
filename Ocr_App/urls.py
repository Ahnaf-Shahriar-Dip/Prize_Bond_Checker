"""
URL configuration for Ocr_App project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ocr.views import *
from home.views import*

from pdf_to_text.views import*



from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static







from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ocr/', upload_image, name='upload_image'),  # Mapping root URL to upload_image view

    path('display_text/', display_text, name='display_text'),
    path('generate_text/', generate_text, name='generate_text'),
    path('', home, name='home'),

    path('save_number/', save_extracted_number_ocr, name='save_extracted_number'),

    path('save_extracted_number/', save_extracted_number_pdf, name='save_extracted_number'),

    path('show_data/', show_data, name='show_data'),

    
    
   
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 