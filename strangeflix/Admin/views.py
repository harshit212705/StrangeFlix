from provider.models import SeriesDetails,SeriesSubCategories,SUB_CATEGORY_TYPES,LANGUAGES_TYPES
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json
# Create your views here.

# renders the admin dashboard page on get request from provider account
@login_required(login_url='home_page')
def admin_dashboard(request):
    if request.method == 'GET' and request.user.user_type == 'A':
        return render(request, 'Admin/admin.html')
    else:
        return render(request, 'templates/404.html')


# get all the series 
@csrf_exempt
@login_required(login_url='home_page')
def get_series(request):
    if request.method == 'POST' and request.user.user_type == 'A':
        series=SeriesDetails.objects.all().order_by('date_of_creation')
        dataToSent=[]
        for val in series:
            data={}
            subcategory=[]
            for sub in SeriesSubCategories.objects.filter(series_id=val.series_id):
                subcategory.append(SUB_CATEGORY_TYPES[sub.sub_category-1][1])
            data.update({str(val.pk):(val.series_id,val.provider_id.pk,val.series_name,val.description,LANGUAGES_TYPES[val.language-1][1],val.CATEGORY_TYPES[val.category-1][1],val.date_of_creation.strftime("%d %b %Y"),val.thumbnail_image.url,subcategory)})
            dataToSent.append(data)
        context={
            'series':dataToSent,
            'is_successful': '',
        }
        context['is_successful'] = 'series fetched successfully!!'
        return JsonResponse(context)
    else:
        return render(request, 'templates/404.html')



