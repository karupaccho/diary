from config import diary
from .forms import InquiryForm
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
import logging
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Diary

# Create your views here.

logger = logging.getLogger(__name__)

# def index(request):
#     return render(request, 'diary/index.html')

class IndexView(generic.TemplateView):
    template_name = "diary/index.html"

class InquiryView(generic.FormView):
    template_name = "diary/inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request,'メッセージを送信しました')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary/diary_list.html'
    paginate_by = 2

    def get_queryset(self):
        diaries = Diary.objects.filter(user = self.request.user).order_by('-created_at')
        return diaries

class DetailView(generic.DeleteView):
    model = Post
    slug_field = "title"
    slug_url_kwarg = "title"

class DiaryDetailView(LoginRequiredMixin,generic.DeleteView):
    model = Diary
    template_name = 'diary/diary_detail.html'
    pk_url_kwarg = 'id'

class DiaryCreateView(LoginRequiredMixin,generic.CreateView):
    model = Diary
    template_name = "diary_create.html"
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit = False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request,'日記を作成しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'日記の作成に失敗しました')
        return super().form_invalid(form)