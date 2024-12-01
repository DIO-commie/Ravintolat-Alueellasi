from django.shortcuts import render

# Create your views here.
# ravintolat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ravintola, Arvostelu
from .forms import ArvosteluForm
from django.contrib.auth.decorators import login_required

def index(request):
    hakusana = request.GET.get('hakusana', '')
    if hakusana:
        ravintolat = Ravintola.objects.filter(nimi__icontains=hakusana)
    else:
        ravintolat = Ravintola.objects.all()
    return render(request, 'ravintolat/index.html', {'ravintolat': ravintolat, 'hakusana': hakusana})

def ravintola_detail(request, ravintola_id):
    ravintola = get_object_or_404(Ravintola, pk=ravintola_id)
    arvostelut = ravintola.arvostelut.all()
    return render(request, 'ravintolat/ravintola_detail.html', {'ravintola': ravintola, 'arvostelut': arvostelut})

@login_required
def lisaa_arvostelu(request, ravintola_id):
    ravintola = get_object_or_404(Ravintola, pk=ravintola_id)
    if request.method == 'POST':
        form = ArvosteluForm(request.POST)
        if form.is_valid():
            arvostelu = form.save(commit=False)
            arvostelu.ravintola = ravintola
            arvostelu.kayttaja = request.user
            arvostelu.save()
            return redirect('ravintola_detail', ravintola_id=ravintola.id)
    else:
        form = ArvosteluForm()
    return render(request, 'ravintolat/lisaa_arvostelu.html', {'form': form, 'ravintola': ravintola})

@login_required
def profiili(request):
    profiili = request.user.profiili
    return render(request, 'ravintolat/profiili.html', {'profiili': profiili})

@login_required
def suosikit(request):
    profiili = request.user.profiili
    suosikit = profiili.suosikit.all()
    return render(request, 'ravintolat/suosikit.html', {'suosikit': suosikit})
