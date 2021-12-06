from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.conf import settings
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
            upload_file = request.FILES['document']
            form.save()
            global doc
            # docu = Document.objects.latest('document')
            doc = upload_file
            #doc = form.cleaned_data.get("document")  # получает текущий элемент
            # doc = File(docu)
            print(type(upload_file))
            #print(doc)
            print(type(upload_file.read()))
            print(type(str(upload_file.read())))
            print(str(upload_file.read()))
            return redirect('main')
    else:
        form = DocumentForm()

    return render(request, 'main.html', {'form': form})


def pars(document):
    x_ = []
    y_ = []
    print(document)
    #document_ = document.file
    #print(type(document_))
    #print(document_.getvalue())
    # document = open(docum, 'r')
    media_dir = settings.MEDIA_ROOT
    root = str(media_dir) + '\\' + 'documents' + '\\' + str(document)
    with open(root) as document:
        for line in document.readlines():

            for line2 in line.split("\n"):

                if not line2.strip():
                    continue

                x, y = [word.strip() for word in line2.split(" ")]
                x_.append(x)
                y_.append(y)

    return x_, y_


def draw(request):
    global doc
    if not doc:
        str = "File is not found"
        return render(request, 'draw.html', {'str': str})
    else:
        x, y = pars(doc)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name='Исходный график'))
        graph = fig.to_html(full_html=False, default_height=500, default_width=500)
        context = {'graph': graph}
        return render(request, 'draw.html', context)
        # HttpResponse("Hi")
