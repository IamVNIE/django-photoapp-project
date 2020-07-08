from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import *

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
import logging

# Get an instance of a logger
log = logging.getLogger(__name__)

#---------- SECURITY and PROTECTION ---------------------------#
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
def media_folder_only(request, **kwargs):
	log.warn('Executing media_folder_only Function')
	print('Executing media_folder_only Function')
	raise PermissionDenied

from django.conf import settings 
def sid(request):
	print('\n\nSID FUNCTION\n\n', request)
	response = HttpResponse()
	response['X-Accel-Redirect'] ='media/images/0.gif'
	return request

def secure_image_delivery(request, username, image_id):
	print('Executing This Function')
	log.warn('Executing SID: User-{} image-{}'.format(username, image_id))
	if username == request.user:
		validAccess = 1
	else:
		validAccess = 0
	if validAccess:
		response = HttpResponse()
		response['X-Accel-Redirect'] = 'media/images/'+image_id
		#response['Content-Disposition'] = 'attachment; filename="{}"'.format(image_id)
		return response
	else:
		raise PermissionDenied
# Create your views here.
def index(request):
    return render(request, 'base.html')

# Create your views here.
def home(request):
	userName = request.user
	return render(request, 'base.html', {'userName':userName})

from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
class PhotosUploadView(CreateView):
	form_class = PhotosUploadForm
	template_name = 'upload.html'
	success_url = '/list/'
	def form_valid(self, form):
		exp = form.save(commit=False)
		exp.creator = self.request.user
		exp.image =  exp.image
		exp.uploaded_at = timezone.now()
		exp.save()
		idk = exp.id
		return HttpResponseRedirect(self.get_success_url(idk))

	def get_success_url(self, idk):
		return reverse_lazy('userManager:details',kwargs={'pk': idk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['userName'] = self.request.user
		return context

from django.http import HttpResponse

class PhotosHDView(DetailView):
	model = MYPhotos
	template_name = 'detail.html'
	context_object_name  = 'photos'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['userName'] = self.request.user
		return context


class PhotosListview(ListView):
	model = MYPhotos
	paginate_by = 6
	template_name= 'list.html'
	context_object_name  = 'photos'
	def get_queryset(self):
		return self.model.objects.filter(
									creator=self.request.user).order_by(
										'-uploaded_at'
										)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['userName'] = self.request.user
		return context

# Create your views here.
def register(response):
	if response.method == "POST":
		form = SignUpForm(response.POST)
		if form.is_valid():
			print('Form is Valid')
			form.save()

		return redirect("/accounts/login")
	else:
		form = SignUpForm()
		return render(response, "userManager/register.html", {"form":form})