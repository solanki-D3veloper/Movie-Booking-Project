from django.shortcuts import render
from accounts.models import *
from django.core.files.storage import FileSystemStorage
import qrcode
from io import BytesIO
from django.conf import settings
from datetime import datetime
import os
from django.http import JsonResponse
from . import models

# Create your views here.


def index(request):
    movies = Movie.objects.all()
    context = {
        'mov': movies
    }
    return render(request,"index.html", context)

def movies(request, id):
    #cin = Cinema.objects.filter(shows__movie=id).distinct()
    movies = Movie.objects.get(movie=id)
    cin = Cinema.objects.filter(cinema_show__movie=movies).prefetch_related('cinema_show').distinct()  # get all cinema
    show = Shows.objects.filter(movie=id)
    date = Shows.objects.filter(movie=id)
    context = {
        'movies':movies,
        'show':show,
        'cin':cin,
        'date':date,
    }
    return render(request, "movies.html", context )

def seat(request, id):
    show = Shows.objects.get(shows=id)
    seat = Bookings.objects.filter(shows=id)
    return render(request,"seat.html", {'show':show, 'seat':seat})    

def booked(request):
    if request.method == 'POST':
        user = request.user
        seat = ','.join(request.POST.getlist('check'))
        show = request.POST['show']
        book = Bookings(useat=seat, shows_id=show, user=user)
        book.save()
        return render(request,"booked.html", {'book':book})    
        

def ticket(request, id):
    ticket = Bookings.objects.get(id=id)
    print(ticket.shows.price)
    if ticket.useat:  # Ensure the field is not empty or None
        seats = ticket.useat.split(',')  # Split the string by commas
        seats_count = len(seats)  # Count the number of items
    else:
        seats_count = 0
    amount = ticket.shows.price * seats_count
    
    gpay_url = f"upi://pay?pa=solankidharmesh901@okaxis&pn=Dharmesh%20Solanki&am={amount}&cu=INR&aid=uGICAgMCLyv3aIA"

    qr = qrcode.make(gpay_url)

    img_io = BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)

    # Save it to a temporary location or serve directly
    c_path = settings.BASE_DIR + settings.MEDIA_URL 
    folder_path = os.path.join(c_path, 'tmp').replace('\\', '/')

    fs = FileSystemStorage(location=folder_path)  # Save temporarily to /tmp or any other location
    filename = f"ticket_qr_{id}.png"
    f_path = fs.save(filename, img_io)
    # Generate the image URL (to be passed to the template)
    image_url = os.path.join(settings.MEDIA_URL, "tmp", filename).replace('\\', '/')

    return render(request,"ticket.html", {'ticket':ticket,'qr_image_url': image_url, 'total_amount':amount})

def fetch_shows(request):
    date = request.GET.get('date')
    movie_id = request.GET.get('movie_id')

    if date and movie_id:
        # Use filter() to get multiple shows for the selected date and movie
        shows = Shows.objects.filter(date=date, movie_id=movie_id)
        show_data = [
            {
                'shows': show.shows,  # Show ID
                'time': show.time,  # Show time
                'cinema_name': show.cinema.cinema_name,  # Cinema name
            }
            for show in shows
        ]
        return JsonResponse({'shows': show_data}, safe=False)

    # Return an empty list if no shows are found
    return JsonResponse({'shows': []}, safe=False)