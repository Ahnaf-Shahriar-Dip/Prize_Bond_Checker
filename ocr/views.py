from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pytesseract
from PIL import Image
import re
import io



from .models import * 


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cropped_image = request.FILES.get('cropped_image')
        print(cropped_image)  # Add this line to print the cropped image
        if cropped_image:
            extracted_text = perform_ocr(cropped_image)
            return JsonResponse({'success': True, 'extracted_text': extracted_text})
        else:
            return JsonResponse({'success': False, 'message': 'No image file received.'})
    return render(request, 'upload_image.html')




#If i want to etract all

#def perform_ocr(image):
    #img = Image.open(image)
    #text = pytesseract.image_to_string(img, lang='ben+eng')
    #return text




#I have used REGEX to find aonly number from all text

def perform_ocr(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img, lang='ben+eng')

    # Use regular expression to extract numerical values
    numerical_values = re.findall(r'\d+', text)

    # Join the numerical values into a single string
    numerical_text = ''.join(numerical_values)

    print("Number is",numerical_text)

    return numerical_text


from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def save_extracted_number_ocr(request):
    extracted_number = request.POST.get('extracted_number')
    if extracted_number:
        # Create a new ocr_data instance and save it to the database
        ocr_entry = ocr_data(bond_number=extracted_number, method='OCR')
        ocr_entry.save()
        return JsonResponse({'success': True, 'message': 'Number saved successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'No number to save.'})
