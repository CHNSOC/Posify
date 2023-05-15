from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import ImageForm

import os
import subprocess

from .posematching import pose_matching

def index(request):
    template = loader.get_template('keypt_gen/index.html')
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            command = r"bin\openposedemo.exe --image_dir C:\Users\Reychard\Posify_Django\media\images --write_json C:\Users\Reychard\Posify_Django\media\jsons --net_resolution 320x176"
            ret = subprocess.run(command, cwd=r'C:\Users\Reychard\Documents\openpose', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            requestedImageJsonPathFolder = r"C:\Users\Reychard\Posify_Django\media\jsons"
            requestedImageJsonPath = r""
            for x in os.listdir(requestedImageJsonPathFolder):
                if x.endswith(".json"):
                    requestedImageJsonPath = requestedImageJsonPathFolder +"\\"+ x
            displayed_path_sim_dict =  pose_matching.matchImageJSONToImageDatabase(requestedImageJsonPath, 0.7)

            request.session['JSONPath'] = requestedImageJsonPath

            imageDir = r"C:\Users\Reychard\Posify_Django\media\images"
            currImagePath = ""
            for x in os.listdir(imageDir):
                #currImagePath = imageDir + "\\" + x
                currImagePath = "images/" + x
                
            request.session['imgpath'] = currImagePath
            return render(request, 'keypt_gen/imageResult.html', {'form': form, 'img_obj': img_obj, 'dict_of_matched_files' : displayed_path_sim_dict, 'imgpath' : currImagePath})
    else:
        form = ImageForm()
    return render(request, 'keypt_gen/index.html', {'form': form})

def resetImage(request):

    imageDir = r"C:\Users\Reychard\Posify_Django\media\images"
    for x in os.listdir(imageDir):
            os.remove(imageDir +"\\"+ x)
    JSONDir = r"C:\Users\Reychard\Posify_Django\media\jsons"
    for x in os.listdir(JSONDir):
         if x.endswith(".json"):
            os.remove(JSONDir +"\\"+ x)
    return redirect('index')

def reSearchWithNewThreshold(request):
    if request.method == 'POST':
        newThres = request.POST.get('simSlider')

        try:
            newThres = float(newThres)
        except ValueError:
            newThres = 0.6
            print("Invalid input -> reset to 0.6")

        currJson = request.session.get('JSONPath')
        currImagePath = request.session.get('imgpath')
        displayed_path_sim_dict =  pose_matching.matchImageJSONToImageDatabase(currJson, float(newThres))

        return render(request, 'keypt_gen/imageResult.html', {'dict_of_matched_files' : displayed_path_sim_dict, 'imgpath' : currImagePath})
def testImageResult(request):
    template = loader.get_template('keypt_gen/imageResult.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))

def moveUserImageToTemp():
    imageDir = r"C:\Users\Reychard\Posify_Django\media\images"
    tempUserImageDir = r"C:\Users\Reychard\Posify_Django\keypt_gen\static\keypt_gen\tempUserImage"
    for x in os.listdir(imageDir):
        os.rename(imageDir +"\\"+ x, tempUserImageDir +"\\"+ x)
