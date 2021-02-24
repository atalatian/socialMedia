from django.shortcuts import render, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic import DetailView
from .models import User
from .models import Post
from .forms import UserForm


# Create your views here.
def index(request):
    return HttpResponse('ok')


class UserCreate(CreateView):
    model = User
    form_class = UserForm
    template_name = 'socialMediaApp/signUp.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.id,))


class UserDetail(DetailView):
    model = User
    template_name = 'socialMediaApp/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.filter(pk=self.kwargs['pk']).first()
        context['post_list'] = User.objects.filter(pk=self.kwargs['pk']) \
            .first().post_set.all()
        return context


class UserEnter(FormView):
    model = User
    form_class = UserForm
    template_name = 'socialMediaApp/LogIn.html'
    message = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        return context

    def get(self, request, *args, **kwargs):
        if self.kwargs['state'] == 'accept':
            self.message = 'Enter your email and password.'
        return super(UserEnter, self).get(request, *args, **kwargs)


