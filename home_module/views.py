from django.shortcuts import render
from django.views.generic import TemplateView



# Create your views here.
def home(request):
    return render(request, 'home_module/index_page.html')

class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'