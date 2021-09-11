from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from datetime import date,datetime
from .models import User, plan_trip


@login_required
def index(request):
    all_user_trips = plan_trip.objects.all().filter(creator__id = request.session['user']['id']) 
    that_u_join =  plan_trip.objects.all().filter(join_trip__id = request.session['user']['id'])
    all_join = plan_trip.objects.exclude(creator__id =  request.session['user']['id'])
    context = {
        'user_trip': all_user_trips,
        'another': that_u_join,
        'all_join': all_join
    }
    return render(request, 'index.html', context)

@login_required
def new_trip(request):
    #me aseguro que no seleccione fechas en el pasado
    now = datetime.now()
    date_time = now.strftime('%Y-%m-%d')
    if request.method == 'GET':
        now = datetime.now()
        date_time = now.strftime('%Y-%m-%d')
        data = {
            'now' : date_time
        }
        return render(request, 'new_trip.html', data)

    destino = request.POST['destino']
    descripcion = request.POST['desc']
    inicio = request.POST['fecha_inicio']
    termino = request.POST['fecha_termino']

    if inicio == date_time and termino == date_time:
        messages.error(request,'Seleccione fechas distintas')
        return redirect('/travels/add')
    if inicio  == termino:
        messages.error(request,'La fecha de inicio o termino deben ser distintas')
        return redirect('/travels/add')
    if inicio>termino:
        messages.error(request,'Are u kidding me??')
        messages.error(request,'la fecha de termino debe ser mas a futuro')
        return redirect('/travels/add')

    traer_user = User.objects.get(id = request.session['user']['id'])
    new_plan = plan_trip.objects.create(
        destination = destino, 
        description = descripcion, 
        travel_date_from = inicio, 
        travel_date_to = termino,
        creator= traer_user
        )
    messages.success(request,'plan creado con exito!')
    return redirect('/')

@login_required
def delete_plan(request,id_p):
    id_user = request.session['user']['id']
    plan = plan_trip.objects.get(id = id_p)
    if id_user == plan.creator.id:
        plan.delete()
        messages.success(request,'Appointment deleted')
        return redirect('/')
    messages.error(request,'No puedes eliminar el plan de viaje de los demas')
    return redirect('/')

@login_required
def show_details(request,id_p):
    bring_plan = plan_trip.objects.get(id = id_p)
    data = {
        'trip': bring_plan
    }
    return render(request,'show_plan.html', data)

@login_required
def join_trip(request,id_p):
    bring_plan =  plan_trip.objects.get(id = id_p)
    id_user = request.session['user']['id']
    bring_user = User.objects.get(id = id_user)

    bring_plan.join_trip.add(bring_user)
    bring_plan.save()
    messages.success(request, 'Incorporacion al viaje correctamente')
    return redirect('/')

@login_required
def left_trip(request,id_p):
    bring_plan = plan_trip.objects.get(id = id_p)
    bring_user = User.objects.get(id = request.session['user']['id'])
    bring_plan.join_trip.remove(bring_user)
    bring_plan.save()
 
    messages.success(request, 'Te saliste de este viaje correctamente')
    return redirect('/')

    
    
