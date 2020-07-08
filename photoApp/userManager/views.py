from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import *

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
import logging
import os
# Get an instance of a logger
log = logging.getLogger(__name__)

#---------- SECURITY and PROTECTION ---------------------------#
from django.http import HttpResponse
from django.http import HttpResponseForbidden

def media_access(request, path):
	access_granted = False
	print('Media Access Cleanser Triggered',path)
	log.info('Media Access Cleanser Triggered', request,path)
	user = request.user
	if path !='':
		tags = path.split('/')
		if len(tags)>1:
			if user.is_authenticated:
				id = tags[1]
				try:
					id = str(id)
					fileName = os.path.basename(path)
					q = get_object_or_404(MYPhotos ,pk=id)
					print('Req User: {} -- Image Owner: {}'.format(user, q.creator))
					if user == q.creator:
						access_granted = True
					elif q.is_public:
						access_granted = True
					elif user.is_superuser:
						# If admin, everything is granted
						access_granted = True
				except:
					log.error('Requested Media - Not a Valid Path')

	if access_granted:
		response = HttpResponse()
		del response['Content-Type']
		response['X-Accel-Redirect'] = '/protected/' + path.replace(str(id)+'/','')
		print('Final Response', response['X-Accel-Redirect'])
		return response
	else:
		return HttpResponseForbidden('Not authorized to access this media.')

from django.conf import settings 
from django.shortcuts import get_object_or_404
#from sendfile import sendfile

def sid(request, image_name):
	print('\n\nSID FUNCTION\n\n', request, image_name)
	log.info('SID FUNCTION', request,image_name)

	response = HttpResponse('')
	privateFileName = 'media/images/{}'.format(image_name)
	#q = get_object_or_404(MYPhotos, pk=image_name)

	print('privateFileName', privateFileName)
	response['Content-Type'] = ''
	response['X-Accel-Redirect'] =privateFileName # q.image.url

	print('Response X ',response)
	return response


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
		x = context[self.context_object_name]
		context['safeURLs'] = x.image.url.replace('/images','/images/'+str(x.id))
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
		print(10*'-','Context')
		context['safeURLs'] =[]
		for x in context[self.context_object_name]:
			context['safeURLs'].append(x.image.url.replace('/images','/images/'+str(x.id)))
		print(10*'-')
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