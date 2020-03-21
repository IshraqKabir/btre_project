from django.shortcuts import render, get_object_or_404
from .models import Contact
from django.contrib import messages
from listings.models import *
# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST.get('listing', False)
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id)
            
            if has_contacted:
                messages.error(request, 'You have alreay made an inquiry for this listing')
                return render(request, '/listings/'+listing_id)
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email,phone=phone,message=message,user_id=user_id)

        contact.save()

        listing = get_object_or_404(Listing, pk=listing_id)
        context = {
        'listing': listing,

        }
        messages.success(request, 'You request has been submitted, a realtor will get back to you soon')
        return render(request, 'listings/listing.html', context)
