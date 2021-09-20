from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Skate, Place, Photo, Maintenance
from .forms import MaintenanceForm
from django.views.generic import ListView, DetailView
import uuid
import boto3
import os
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    # return HttpResponse('<h1>Skate Collector</h1>')
    return render(request, 'about.html')

def about(request):
    # return HttpResponse('<h1>About Skates</h1>')
    return render(request, 'about.html')

@login_required
def skates_index(request):
    # return HttpResponse('<h1>skates index</h1>')
    # skates = Skate.objects.all()
    skates = Skate.objects.filter(user=request.user)
    return render(request, 'skates/index.html', {'skates': skates})

@login_required
def skate_detail(request, skate_id):
    skate = Skate.objects.get(id=skate_id)
    places_not_skating = Place.objects.exclude(id__in = skate.places.all().values_list('id'))
    maintenance_form = MaintenanceForm()
    return render(request, 'skates/detail.html', {'skate': skate, 'maintenance_form': maintenance_form, 'places': places_not_skating})

class SkateCreate(LoginRequiredMixin, CreateView):
    model = Skate
    fields = ['nickname', 'brand', 'style', 'color', 'plates', 'stops', 'wheels', 'bearings', 'cushions', 'slides']
    success_url = '/skates/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SkateUpdate(LoginRequiredMixin, UpdateView):
    model = Skate
    fields = ['brand', 'style', 'color', 'plates', 'stops', 'wheels', 'bearings', 'cushions', 'slides']


class SkateDelete(LoginRequiredMixin, DeleteView):
    model = Skate
    success_url = '/skates/'

@login_required
def add_maintenance(request, skate_id):
    form = MaintenanceForm(request.POST)

    if form.is_valid():
        new_maintenance = form.save(commit=False)
        new_maintenance.skate_id = skate_id
        new_maintenance.save()
        print(f"saved form")

    return redirect('detail', skate_id=skate_id)

# @login_required
# def remove_maintenance(request, skate_id):
#     all_logs_for_this_skate = Maintenance.objects.filter(skate=skate_id)
#     print(all_logs_for_this_skate)
#     # the deletes all maintenance logs associated with the skate
#     # to fix: update query to return the specific maintenance id and delete by the maintenance id
#     # tried this but was getting errors about 'reverse'
#     # tried adding a reverse function to the Maintenance model in models.py but that didn't work either. will revisit this.
#     all_logs_for_this_skate.delete()
#
#     return redirect('detail', skate_id=skate_id)

class PlaceList(LoginRequiredMixin, ListView):
  model = Place

class PlaceDetail(LoginRequiredMixin, DetailView):
  model = Place

class PlaceCreate(LoginRequiredMixin, CreateView):
  model = Place
  fields = '__all__'

class PlaceUpdate(LoginRequiredMixin, UpdateView):
  model = Place
  fields = '__all__'

class PlaceDelete(LoginRequiredMixin, DeleteView):
  model = Place
  success_url = '/places'

@login_required
def assoc_place(request, skate_id, place_id):
    Skate.objects.get(id=skate_id).places.add(place_id)
    return redirect('detail', skate_id=skate_id)

@login_required
def remove_place(request, skate_id, place_id):
    Skate.objects.get(id=skate_id).places.remove(place_id)
    return redirect('detail', skate_id=skate_id)

@login_required
def add_photo(request, skate_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, skate_id=skate_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', skate_id=skate_id)

def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('skates')
        else:
            error_message = 'Invalid sign up - Try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
