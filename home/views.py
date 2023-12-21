from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
import requests
from django.http import HttpResponseRedirect, HttpResponseRedirect, JsonResponse
from .models import Setting,FAQ,ContactMessage,ContactForm
from django.contrib import messages
from .forms import NewQuestionForm
from django.template.loader import render_to_string
from BrainBuffet import settings
from django.core.mail import EmailMessage


#api-q00J2+cyYHfDCZWwQU1vCA==zbqhtoBjuTgEdiPi
#qusXS1v80ieHbtd/YcVnZA==viZKI2nQeFrb6uJt
# Create your views here.


def index(request):
    setting=Setting.objects.get(pk=1)
    return render(request,'home.html',{'setting':setting})
'''
def index(request):
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(
            api_url + query, headers={'X-Api-Key': 'q00J2+cyYHfDCZWwQU1vCA==zbqhtoBjuTgEdiPi'})
        try:
            api = json.loads(api_request.content)

            print(len(api))
            #print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'food.html', {'api': api})
    else:
        return render(request, 'food.html', {'query': 'Enter a valid query'})
    return render(request, 'food.html', {})
'''


@login_required(login_url='/login')
def community(request):
    return render(request, 'content.html', {})


def faq(request):
    faq = FAQ.objects.filter(status="True")

    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.save()
                messages.success(request, 'Your Question is sent')
        except Exception as e:
            print(e)
            raise

    context = {
        'faq': faq, 'form': form,
    }

    return render(request, 'faq.html', context)


def contactus(request):
    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table

            template = render_to_string('contactmail.html',{'subject': data.subject, 'message': data.message,
                                                            'name': data.name,})
            email = EmailMessage(
                'Contact Message',
                template,
                data.email,
                [settings.EMAIL_HOST_USER],
            )
            email.fail_silently = False
            email.send()
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/')

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context={'setting':setting,'form':form}
    return render(request, 'contactus.html', context)