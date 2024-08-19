# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import MedicalMissionaryDailyReport,BibleWorkerDailyReport
from .forms import BibleWorkerDailyReportForm,MedicalMissionaryDailyReportForm

def bible_worker_daily_report_list(request):
    posts = BibleWorkerDailyReport.objects.all()
    return render(request, 'evangelism/bible_worker_daily_report_list.html', {'posts': posts})

def bible_worker_daily_report_create(request):
    if request.method == 'POST':
        form = BibleWorkerDailyReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bible_worker_daily_report_list')
    else:
        form = BibleWorkerDailyReportForm()
    return render(request, 'evangelism/bible_worker_daily_report_form.html', {'form': form})

def bible_worker_daily_report_update(request, pk):
    post = get_object_or_404(BibleWorkerDailyReport, pk=pk)
    if request.method == 'POST':
        form = BibleWorkerDailyReportForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('bible_worker_daily_report_list')
    else:
        form = BibleWorkerDailyReportForm(instance=post)
    return render(request, 'evangelism/bible_worker_daily_report_form.html', {'form': form})

def bible_worker_daily_report_delete(request, pk):
    post = get_object_or_404(BibleWorkerDailyReport, pk=pk)
    post.delete()
    return redirect('bible_worker_daily_report_list')



def medical_missionary_daily_report_list(request):
    posts = MedicalMissionaryDailyReport.objects.all()
    return render(request, 'evangelism/medical_missionary_daily_report_list.html', {'posts': posts})

def medical_missionary_daily_report_create(request):
    if request.method == 'POST':
        form = MedicalMissionaryDailyReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_missionary_daily_report_list')
    else:
        form = MedicalMissionaryDailyReportForm()
    return render(request, 'evangelism/medical_missionary_daily_report_form.html', {'form': form})

def medical_missionary_daily_report_update(request, pk):
    post = get_object_or_404(MedicalMissionaryDailyReport, pk=pk)
    if request.method == 'POST':
        form = MedicalMissionaryDailyReportForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('medical_missionary_daily_report_list')
    else:
        form = MedicalMissionaryDailyReportForm(instance=post)
    return render(request, 'evangelism/medical_missionary_daily_report_form.html', {'form': form})

def medical_missionary_daily_report_delete(request, pk):
    post = get_object_or_404(MedicalMissionaryDailyReport, pk=pk)
    post.delete()
    return redirect('medical_missionary_daily_report_list')
