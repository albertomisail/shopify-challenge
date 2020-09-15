from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from fuzzywuzzy import fuzz

from imageproject.models import Transaction, Image

from .forms import LoadBalanceForm, UploadForm, SearchForm

def home(request):
    return render(request, 'home.html')

def loadbalance(request): 
    if request.method == 'POST':
        form = LoadBalanceForm(request.POST)
        if form.is_valid():
            balance = form.cleaned_data['balance']
            if balance <= 0:
                return HttpResponseBadRequest('balance should be positive')
            user = get_user(request)
            profile = user.profile
            profile.balance += balance
            profile.save()
            return redirect('home')
    else:
        form = LoadBalanceForm()

    return render(request, 'loadbalance.html', {'form': form})

def delete_image(request, image_id): 
    context ={} 
    image = get_object_or_404(Image, pk=image_id) 
    if image.owner == get_user(request): 
        image.deleted = True
        print('here')
        image.save()
    else:
        return HttpResponse('not your image')
    return redirect('home')

def buy_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    user = get_user(request)
    profile = user.profile
    if image.owner == None:
        return HttpResponse('cannot buy this image')
    if profile.balance < image.price:
        return HttpResponse('not enough balance')
    profile.balance -= image.price
    profile.save()
    Transaction.objects.create(buyer=user, image=image, bought_date=timezone.now())
    return redirect('home')

def search(request): 
    images = Image.objects.filter(deleted=False)
    THRESHOLD = 50
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            filtered_images = []
            for image in images: 
                if fuzz.ratio(search, image.title) > THRESHOLD: 
                    filtered_images.append(image.id)
            images = Image.objects.filter(id__in=filtered_images)
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form, 'images': images})

def upload_new(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            Image.objects.create(image=image, title=title, publish_date=timezone.now(), owner=get_user(request), price=price)
            return redirect('home')
    else:
        form = UploadForm()

    return render(request, 'upload_new.html', {'form': form})

class UploadListView(ListView): 
    context_object_name = 'Image'

    def get_queryset(self):
        queryset = Image.objects.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        return context
        
class PurchaseListView(ListView): 
    model = Transaction
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        return context