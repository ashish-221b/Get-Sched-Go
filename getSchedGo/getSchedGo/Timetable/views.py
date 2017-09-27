from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import DailySched, Event, Slots
