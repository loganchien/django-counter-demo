import random
import time

from django.db import transaction
from django.db.models import F
from django.shortcuts import HttpResponse

from .models import Counter


def counter1(request):
    # Incorrect values.

    counter = Counter.objects.get_or_create(pk=1)[0]
    counter.num_counts += 1
    counter.save()

    return HttpResponse(str(counter.num_counts), content_type='text/plain')


def counter2(request):
    # Database has the correct value but users may get incorrect values.

    counter = Counter.objects.get_or_create(pk=2)[0]
    counter.num_counts = F('num_counts') + 1
    counter.save()

    counter.refresh_from_db()

    return HttpResponse(str(counter.num_counts), content_type='text/plain')


def counter3(request):
    # Database has the correct value but users may get incorrect values.

    counter = Counter.objects.get_or_create(pk=3)[0]
    counter.num_counts = F('num_counts') + 1
    counter.save()

    # Demonstrate race condition by sleeping randomly between save() and
    # refresh_from_db().
    time.sleep(random.randint(0, 5) / 1000)

    counter.refresh_from_db()

    return HttpResponse(str(counter.num_counts), content_type='text/plain')


def counter4(request):
    # Correct version.

    Counter.objects.get_or_create(pk=4)

    with transaction.atomic():
        counter = Counter.objects.filter(id=4).select_for_update()[0]
        num_counts = counter.num_counts + 1
        counter.num_counts = num_counts
        counter.save()

    return HttpResponse(str(num_counts), content_type='text/plain')
