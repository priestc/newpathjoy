import datetime
import random
import json

from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import (StepOneForm, StepTwoForm, StepThreeForm, StepFourForm,
    StepFiveForm, StepSixForm, StepSevenForm, StepEightForm)
from .models import (StepOne, StepTwo, StepThree, StepFour, StepFive, StepSix,
    StepSeven, StepEight, CompletedBooking)

step_forms = {
    1: StepOneForm,
    2: StepTwoForm,
    3: StepThreeForm,
    4: StepFourForm,
    5: StepFiveForm,
    6: StepSixForm,
    7: StepSevenForm,
    8: StepEightForm,
}

step_models = {
    1: StepOne,
    2: StepTwo,
    3: StepThree,
    4: StepFour,
    5: StepFive,
    6: StepSix,
    7: StepSeven,
    8: StepEight,
}

TOTAL_STEPS = 8

def step(request, step_number):
    step_number = int(step_number)
    Form = step_forms[step_number]
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            if not request.session.exists(request.session.session_key):
                request.session.create()
            session_obj = Session.objects.get(session_key=request.session.session_key)
            s.session = session_obj
            s.save()

            next_step = step_number + 1
            if next_step <= TOTAL_STEPS:
                # go to next step
                url = reverse('step', args=[next_step])
                return HttpResponseRedirect(url)
            else:
                # go to confirmation page
                booking = complete_booking(session_obj)
                url = reverse('see', args=[booking.key])
                return HttpResponseRedirect(url)
    else:
        form = Form()

    if step_number == TOTAL_STEPS:
        # last step
        template = "payment_step.html"
    else:
        template = "step.html"

    return render_to_response(template, {'form': form, "step": step_number}, RequestContext(request))

def complete_booking(session):
    steps = {}
    for step in xrange(1, TOTAL_STEPS + 1):
        StepModel = step_models[step]
        step_obj = StepModel.objects.filter(session=session).latest()
        step_obj.session = None
        step_obj.save()
        steps["step%s" % step] = step_obj

    key = session.session_key
    if CompletedBooking.objects.filter(key=key).exists():
        # if more than one booking exists for a session
        key = "%s%d" % (key, random.random() * 1e12)

    return CompletedBooking.objects.create(key=key, **steps)

def cancel_booking(request, key):
    CompletedBooking.objects.filter(key=key).update(canceled=True)
    return HttpResponseRedirect('/')

def see_booking(request, key):
    booking = CompletedBooking.objects.get(key=key)
    return render_to_response("new_booking.html", {'booking': booking}, RequestContext(request))

def available_times(request):
    times = [
        datetime.datetime(2013, 1, 4, 8, 45).isoformat(),
        datetime.datetime(2013, 1, 4, 9, 30).isoformat(),
        datetime.datetime(2013, 1, 5, 10, 00).isoformat(),
        datetime.datetime(2013, 1, 5, 10, 45).isoformat(),
    ]
    return HttpResponse(json.dumps(times), mimetype="application/json")

