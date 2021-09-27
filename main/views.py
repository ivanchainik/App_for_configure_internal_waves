from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            doc = form.cleaned_data.get("document") #получает текущий элемент
            return redirect('main')
    else:
        form = DocumentForm()

    return render(request, 'main.html', {'form': form})
