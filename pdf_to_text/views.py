
import fitz  # PyMuPDF
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt
from .models import*


# For extract all
#def extract_text_from_pdf(pdf_file):
    #text = ""
    #if isinstance(pdf_file, str):  # If a file path is provided
        #pdf_document = fitz.open(pdf_file)
    #elif hasattr(pdf_file, 'temporary_file_path'):  # If a file object is provided
        #pdf_file_path = pdf_file.temporary_file_path()
        #pdf_document = fitz.open(pdf_file_path)
    #else:
        #raise ValueError("Invalid PDF file")

    #for page_num in range(len(pdf_document)):
        #page = pdf_document.load_page(page_num)
        #text += page.get_text()
    #return text



# only extract bengali and english number

def extract_text_from_pdf(pdf_file):
    text = ""
    if isinstance(pdf_file, str):  # If a file path is provided
        pdf_document = fitz.open(pdf_file)
    elif hasattr(pdf_file, 'temporary_file_path'):  # If a file object is provided
        pdf_file_path = pdf_file.temporary_file_path()
        pdf_document = fitz.open(pdf_file_path)
    else:
        raise ValueError("Invalid PDF file")

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    # Define regex pattern for Bengali and English numbers
    numbers_pattern = r'[০১২৩৪৫৬৭৮৯0-9]+'

    # Find all occurrences of Bengali and English numbers in the text
    numbers = re.findall(numbers_pattern, text)

    # Combine the results and remove duplicates
    all_numbers = list(set(numbers))
    
    return ' '.join(all_numbers)


def display_text(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        pdf_file_path = os.path.join(fs.location, filename)
        pdf_path = fs.url(filename)
        extracted_text = extract_text_from_pdf(pdf_file_path)
        fs.delete(filename)
        return render(request, 'display_text.html', {'pdf_path': pdf_path, 'extracted_text': extracted_text})
    return render(request, 'display_text.html')


import tempfile

def generate_text(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            # Save the uploaded PDF file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in pdf_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            extracted_text = extract_text_from_pdf(temp_file_path)
            # Clean up by deleting the temporary file
            os.unlink(temp_file_path)
            return JsonResponse({'extracted_text': extracted_text})
        else:
            return JsonResponse({'error': 'PDF file not found in request'})
    else:
        return JsonResponse({'error': 'Invalid request'})





@csrf_exempt
def save_extracted_number_pdf(request):
    if request.method == 'POST':
        extracted_number = request.POST.get('extracted_number')
        if extracted_number:
            ocr_entry = ocr_data(bond_number=extracted_number, method="PDF")
            ocr_entry.save()
            return JsonResponse({'success': True, 'message': 'Number saved successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'No number to save.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})