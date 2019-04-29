from django.urls import path
from bbc.views import ArticlesView, detail_view, mp3, contact, home, faq
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('blog/', ArticlesView.as_view(context_object_name = 'news'), name='blog' ),
    path('', home, name='home'),
    path('faq/', faq, name='faq'),
    path('contact/', contact, name='contact'),
    path('audio/<int:id>/', mp3, name='mp3'),
    path('<slug:slug>/', detail_view, name='detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
