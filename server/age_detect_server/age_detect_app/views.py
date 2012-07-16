from age_detect_app.models import UploadedImage
from django.core.context_processors import csrf
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response

class UploadFileForm(forms.Form):
    udid = forms.CharField(initial = '12345')
    image  = forms.FileField()


def upload_file(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadedImage = UploadedImage()
            uploadedImage.handle_uploaded_file(request.POST['udid'], request.FILES['image'])
            result = uploadedImage.to_json()#get age
            uploadedImage.cleanup()#remove all tmp files used to get age
            response = HttpResponse(result, mimetype = "application/json")
            return response
    else:
        form = UploadFileForm()
        c['form'] = form
        return render_to_response('upload.html', c)