from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import pandas as pd
import openpyxl
import xlrd

doc = None


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            doc = form.cleaned_data.get("document")  # получает текущий элемент
            return redirect('main')
    else:
        form = DocumentForm()

    return render(request, 'main.html', {'form': form})


def pars(document):
    x_ = []
    y_ = []

    for line in document.readlines():

        for line2 in line.split("\n"):

            if not line2.strip():
                continue

            x, y = [word.strip() for word in line2.split(" ")]
            x_.append(x)
            y_.append(y)

    return x_, y_


def draw(request):
    if not doc:
        pass
    else:
        x, y = pars(doc)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name='Исходный график'))
        graph = fig.to_html(full_html=False, default_height=500, default_widht=700)
        context = {'graph': graph}
        return render(request, 'draw.html', context)
