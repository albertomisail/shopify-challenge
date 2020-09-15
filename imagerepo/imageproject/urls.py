from django.urls import path
from . import views
from imageproject.views import PurchaseListView, UploadListView
from django.conf import settings
from django.conf.urls.static import static 

# add different views (from views.py) here
urlpatterns = [
    path('', views.home, name='home'),
    path('buy/<int:image_id>', views.buy_image, name='buy'), 
    path('loadbalance', views.loadbalance, name='loadbalance'),
    path('purchases', PurchaseListView.as_view(), name='transaction_list'), 
    path('search', views.search, name='search'), 
    path('uploads', UploadListView.as_view(), name='upload_list'),
    path('upload_new', views.upload_new, name='upload_new'),
    path('delete/<int:image_id>', views.delete_image, name='delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
