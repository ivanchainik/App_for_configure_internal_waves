from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm, ValueForm
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
import math as m
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, firwin, kaiserord, cheb1ord, cheby1, zpk2sos, sosfilt, cheby2, cheb2ord, butter, \
    buttord, ellipord, savgol_filter

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
            # doc = form.cleaned_data.get("document")  # получает текущий элемент
            # doc = File(docu)
            # print(type(upload_file))
            # print(doc)
            # print(type(upload_file.read()))
            # print(type(str(upload_file.read())))
            # print(str(upload_file.read()))
            return redirect('main')
    else:
        form = DocumentForm()

    return render(request, 'main.html', {'form': form})


def pars(document):
    x_ = []
    y_ = []
    # print(document)
    # document_ = document.file
    # print(type(document_))
    # print(document_.getvalue())
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
        x = [float(item) for item in x]
        y = [float(item) for item in y]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Исходный график'))
        graph = fig.to_html(full_html=False, default_height=500, default_width=500)
        context = {'graph': graph}
        return render(request, 'draw.html', context)
        # HttpResponse("Hi")


def get_value(request):
    if request.method == 'POST':
        form2 = ValueForm(request.POST)
        if form2.is_valid():
            cutoff_freq = float(form2.cleaned_data['cutoff_freq'])
            decay_level = int(form2.cleaned_data['decay_level'])
            delta_F = float(form2.cleaned_data['delta_F'])
            Rp = form2.cleaned_data['Rp']
            Rs = form2.cleaned_data['Rs']
            print(cutoff_freq)
            print(decay_level)
            print(delta_F)
            print(Rs)
            print(Rs)
            print(type(cutoff_freq))
            print(type(decay_level))
            print(type(delta_F))
            if(not Rs):
                graph_Hann = Hann(cutoff_freq, decay_level, delta_F)
                return render(request, 'filter.html',
                              {'form2': form2, 'graph_Hann': graph_Hann})
            if(Rs):
                graph_Chebyshev = Chebyshev(cutoff_freq, decay_level, delta_F, Rp, Rs)
                return render(request, 'filter.html',
                              {'form2': form2, 'graph_Chebyshev': graph_Chebyshev})
            # print(font_size)


    else:
        form2 = ValueForm()
        return render(request, 'filter.html', {'form2': form2})


def Hann(cutoff_freq, decay_level, delta_F):
    global doc
    print(doc)
    t = []
    z = []
    root = str(settings.MEDIA_ROOT) + '\\' + 'documents' + '\\' + str(doc)
    with open(root) as document:
        for line in document.readlines():

            for line2 in line.split("\n"):

                if not line2.strip():
                    continue

                t_, z_ = [word.strip() for word in line2.split(" ")]
                t.append(t_)
                z.append(z_)

    t = [float(item) for item in t]
    z = [float(item) for item in z]

    # Global Variables
    Nn = len(z)
    dt = t[2] - t[1]
    fs = 1 / dt  # in Hz
    fN = fs / 2
    fontSize = 14
    #cutoff_freq = 1 / 120  # in Hz
    #delta_F = cutoff_freq / 10
    #decay_level = 30  # in dB

    # Window variables
    delta_F_norm = delta_F / fs
    N = m.ceil(3.3 / delta_F_norm)

    # Original plot
    # plt.plot(t, z)
    # font = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 22}
    # plt.xlabel("t, часы", fontdict=font)
    # plt.ylabel("z, метры", fontdict=font)
    # xo = len(t) / 3600
    # xo = int(xo)
    # plt.xticks(ticks=np.arange(0, len(t), step=3600), labels=np.arange(0, xo + 1, step=1))
    # plt.tick_params(axis='both', which='major', labelsize=16)

    # Window
    b_han = firwin(N, cutoff_freq / fN, window='hann', pass_zero='lowpass')
    y5 = filtfilt(b_han, 1, z)
    # plt.plot(t, y5, color='red')
    # plt.show()
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=t, y=z, mode='lines', name='Original'))
    figure.add_trace(go.Scatter(x=t, y=y5, mode='lines', name='Hann'))
    #figure.show()
    graph1 = figure.to_html(full_html=False, default_height=500, default_width=500)
    return graph1


def Chebyshev(cutoff_freq, decay_level, delta_F, Rp, Rs):
    global doc
    t = []
    z = []
    root = str(settings.MEDIA_ROOT) + '\\' + 'documents' + '\\' + str(doc)
    with open(root) as document:
        for line in document.readlines():

            for line2 in line.split("\n"):

                if not line2.strip():
                    continue

                t_, z_ = [word.strip() for word in line2.split(" ")]
                t.append(t_)
                z.append(z_)
    z = [float(item) for item in z]
    t = [float(item) for item in t]
    # Global Variables
    Nn = len(z)
    dt = t[2] - t[1]
    fs = 1 / dt  # in Hz
    fN = fs / 2
    fontSize = 14
    # cutoff_freq = 1 / 120  # in Hz
    # delta_F = cutoff_freq / 10
    # decay_level = 30  # in dB

    # Window variables
    delta_F_norm = delta_F / fs
    N = m.ceil(3.3 / delta_F_norm)

    # Chebyshev variables
    Wp = cutoff_freq / fN
    Ws = (cutoff_freq + delta_F) / fN
    # Rp = 3
    # Rs = 30  # in dB, decay level for passband and stopband

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=t, y=z, name='Original'))
    xo = len(t) / 3600
    xo = int(xo)
    figure.update_layout(xaxis_title='t, часы',
                         yaxis_title='z, метры',
                         xaxis=dict(
                             tickmode='array',
                             tickvals=np.arange(0, len(t), step=3600),
                             ticktext=np.arange(0, xo + 1, step=1),
                         ))

    N5, Wp1 = cheb1ord(Wp, Ws, Rp, Rs)

    b_cheb = firwin(N5, cutoff_freq / fN, window=('chebwin', Wp1), pass_zero='lowpass')  # STAB 46 Db, need rework
    y9 = filtfilt(b_cheb, 1, z)
    figure.add_trace(go.Scatter(x=t, y=y9, name='Chebyshev'))
    graph = figure.to_html(full_html=False, default_height=500, default_width=500)
    return graph
