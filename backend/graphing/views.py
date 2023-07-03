from django.shortcuts import render

import utils

# Create your views here.
def images(request):
    imgs = utils.get_photos.get_all_photos()



    
