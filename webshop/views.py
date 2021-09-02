from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import paymentForm
from django.contrib.auth.models import User
from accounts.models import Activation
from django import forms
from django_messages.forms import ComposeForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.files.base import ContentFile, File


def payment(request, template_name='payment.html', form_class=ComposeForm):

    ctx = {}

    if request.method == 'POST':
        form_payment = paymentForm(request.POST)
        if form_payment.is_valid():
            recipient_UWP = form_payment.cleaned_data['address']

        form = form_class(request.POST)
        if form.is_valid():
            sender = User.objects.get(username='webshop')

            xml_type = 'invoice'

            via = request.POST['via']
            # Using File
            with open('/peppol-bis-invoice-3.xml') as f:
                xml = self.license_file.save(new_name, File(f))

            if xml:
                print("phre timh")

            if via=='AS4':
                peppol_classic = False
            else:
                peppol_classic = True

            try:
                recipient = Activation.objects.get(webID=recipient_UWP)
                recipient_username = recipient.user.username
                recipient = User.objects.get(username=recipient_username)
            except ObjectDoesNotExist:
                try:
                    recipient = Activation.objects.get(peppolID=recipient_UWP)
                    recipient_username = recipient.user.username
                    recipient = User.objects.get(username=recipient_username)
                except ObjectDoesNotExist:
                    try:
                        recipient = User.objects.get(username=recipient_UWP)
                        recipient_username = recipient.username
                    except ObjectDoesNotExist as e:
                        ctx["errors"] = ["%s" % e]
                        return render(request, template_name, ctx )

            recipient = User.objects.get(pk=recipient.pk)
            sender = User.objects.get(username='webshop')
            form.save(sender=sender , recipient=recipient , xml_type=xml_type,xml=xml, peppol_classic = peppol_classic)
            messages.info(request, _(u"Invoice successfully sent."))
            return HttpResponseRedirect('/')
    else:
        form = paymentForm()

    ctx['form'] = form
    return render(request,template_name,ctx)
