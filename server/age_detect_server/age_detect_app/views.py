from age_detect_app.models import UploadedImage
from django.core.context_processors import csrf
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

class UploadFileForm(forms.Form):
    udid = forms.CharField(initial = '12345')
    language = forms.CharField(initial = 'en')
    image  = forms.FileField()


def upload_file(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadedImage = UploadedImage()
            uploadedImage.cleanup()#remove all tmp files used to get age
            uploadedImage.handle_uploaded_file(request.POST['udid'], request.FILES['image'], request.POST['language'])
            #uploadedImage.handle_uploaded_file('12345', request.FILES['image'])
            result = uploadedImage.to_json()#get age
            #uploadedImage.cleanup()#remove all tmp files used to get age
            response = HttpResponse(result, mimetype = "application/json")
            return response
    else:
        form = UploadFileForm()
        c['form'] = form
        return render_to_response('upload.html', c)

def test(request):
    from age_detect_app.models import AgeGuesser
    #self.get_message(guessed_age, body_part)
    ageGuesser = AgeGuesser()
    guessed_age = {
        'is_male':True,
        'min':0,
        'max':0,
        'age':0,
        'decade':0,
        'is_youth':False,
        'is_old':False,
        'is_20s':True,
        'is_30s':False,
        'language':'en',
        'message': ''
    }
    #body_part = '_forehead'
    #body_part = '_nose_mouth'
    body_part = '_left_eye'
    
    result = json.dumps(ageGuesser.get_message(guessed_age, body_part))
    response = HttpResponse(result, mimetype = "application/json")
    return response
    
