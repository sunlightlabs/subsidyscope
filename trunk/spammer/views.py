from django.conf import settings
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from spammer.models import Recipient
import simplejson
import csv

VALID_RESPONSE_TYPES = ("html", "json")

STATUS_MESSAGES = {
    100: "Success",
    101: "Email address already exists",
    102: "Missing required field",
    103: "Invalid response type",
}

def _render_response(response_type, status=100, message=None, extra_context=None):

    if not message:
        message = STATUS_MESSAGES.get(status, "An unknown error has occurred")
    
    if response_type == "json":

        context = {
            "status": status,
            "message": message,
        }
    
        return HttpResponse(simplejson.dumps(context), content_type="application/json")
        
    #if not status == 100:
    #    return HttpResponseBadRequest("%i %s" % (status, message))
        
    return HttpResponseRedirect(settings.MAILINGLIST_SUBSCRIBED_URL)
    
#
# view methods
#
    
def subscribe(request):
    
    # require POST, otherwise return error
    
    if request.POST:
        
        # get the response type and error if invalid
        
        response_type = request.POST.get("response", "html")
        if response_type not in VALID_RESPONSE_TYPES:
            return _render_response("html", 103)
        
        # check for required fields
            
        if hasattr(settings, "MAILINGLIST_REQUIRED_FIELDS"):
            for field in settings.MAILINGLIST_REQUIRED_FIELDS.keys():
                if not request.POST.get(field, None):
                    message = settings.MAILINGLIST_REQUIRED_FIELDS.get(field, "%s is required" % field)
                    return _render_response(response_type, 102, message=message)

        # get email address and error if invalid or does not exist

        email = request.POST.get("email", None)
        name = request.POST.get("name", None)
        zipcode = request.POST.get("zipcode", None)
        
        try:
        
            recipient = Recipient.objects.get(email=email, subscribed=False)
            recipient.subscribed = True
            recipient.save()
        
        except Recipient.DoesNotExist:
        
            # create and save recipient object
        
            try:
        
                recipient = Recipient(
                    email=email,
                    name=name,
                    zipcode=zipcode
                )
    
                recipient.save()
        
            except IntegrityError:
                return _render_response(response_type, 101)
                
        try:
            if settings.MAILINGLIST_SUBSCRIBE_CALLBACK:
                settings.MAILINGLIST_SUBSCRIBE_CALLBACK(recipient)
        except AttributeError:
            pass
            
        return _render_response(response_type)
    
    raise Http404, u"This is the big leagues, son. I want to see you POST!"
    
def unsubscribe(request, hashcode):
    
    try:
        
        recipient = Recipient.objects.get(hashcode=hashcode)
        
        recipient.subscribed = False
        recipient.save()
        
        context = {u"recipient": recipient}
        
        return render_to_response(u"spammer/unsubscribed.html", context)
        
    except Recipient.DoesNotExist:
        raise Http404, u"We were unable to locate your subscription"
        
def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=subsidyscope-subscribers.csv'
    
    writer = csv.writer(response)
    recipients = Recipient.objects.all()
    for r in recipients:
        row = [r.email]
        writer.writerow(row)

    return response