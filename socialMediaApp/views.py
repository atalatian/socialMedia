from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic.edit import CreateView, FormView
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from .models import User
from .models import Post
from .forms import UserForm
from .forms import PostForm
from .forms import SearchForm
from django.views import View
import json


class auth:
    def __init__(self):
        self.state = {
            'loggedIn': False,
            'pk': None,
        }

    def getState(self):
        return self.state

    def setState(self, loggedIn, pk):
        state = self.state.copy()
        state['loggedIn'] = loggedIn
        state['pk'] = pk
        self.state = state

instance = auth()


# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse_lazy('logIn'))


class UserCreate(CreateView):
    model = User
    form_class = UserForm
    template_name = 'socialMediaApp/signUp.html'

    def get_success_url(self):
        instance.setState(True, self.object.id)
        return reverse_lazy('profile', args=(self.object.id,))


class UserDetail(DetailView, FormMixin):
    model = User
    template_name = 'socialMediaApp/profile.html'
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        if instance.getState()['loggedIn'] and instance.getState()['pk'] == self.kwargs['pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.filter(pk=self.kwargs['pk']).first()
        context['post_list'] = User.objects.filter(pk=self.kwargs['pk']) \
            .first().post_set.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = get_object_or_404(User, email=form.cleaned_data['search'])
        self.success_url = reverse_lazy('viewProfile', args=(self.kwargs['pk'], user.pk))
        return super(UserDetail, self).form_valid(form)


class ViewUserDetail(DetailView):
    model = User
    template_name = 'socialMediaApp/profile.html'

    def get(self, request, *args, **kwargs):
        if instance.getState()['loggedIn'] and instance.getState()['pk'] == self.kwargs['foreignUser_pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.filter(pk=self.kwargs['pk']).first()
        context['post_list'] = User.objects.filter(pk=self.kwargs['pk']) \
            .first().post_set.all()
        context['foreignUser_pk'] = self.kwargs['foreignUser_pk']
        return context


class UserEnter(FormView):
    model = User
    form_class = UserForm
    template_name = 'socialMediaApp/LogIn.html'

    def form_valid(self, form):
        user = get_object_or_404(User, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        self.success_url = reverse_lazy('profile', args=(user.pk,))
        instance.setState(True, user.pk)
        return super().form_valid(form)


class PostCreate(FormView):
    model = Post
    form_class = PostForm
    template_name = 'socialMediaApp/createPost.html'

    def get(self, request, *args, **kwargs):
        if instance.getState()['loggedIn'] and instance.getState()['pk'] == self.kwargs['pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        post = Post.objects.create(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            user_id=self.kwargs['pk']
        )
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.kwargs['pk']
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'socialMediaApp/postDetail.html'

    def get(self, request, *args, **kwargs):
        if instance.getState()['loggedIn'] and instance.getState()['pk'] == self.kwargs['pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Post.objects.get(user_id=self.kwargs['pk'], pk=self.kwargs['post_pk'])
        context['user_pk'] = self.kwargs['pk']
        return context


class ViewPostDetail(DetailView):
    model = Post
    template_name = 'socialMediaApp/postDetail.html'

    def get(self, request, *args, **kwargs):
        if instance.getState()['loggedIn'] and instance.getState()['pk'] == self.kwargs['foreignUser_pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Post.objects.get(user_id=self.kwargs['pk'], pk=self.kwargs['post_pk'])
        context['foreignUser_pk'] = self.kwargs['foreignUser_pk']
        context['user_pk'] = self.kwargs['pk']
        return context


class AutoCompleteView(View):
    def get(self, request):
        if request.is_ajax():
            q = request.GET.get('term', '').capitalize()
            search_qs = User.objects.filter(email__startswith=q)
            results = []
            for r in search_qs:
                results.append(r.email)
            data = json.dumps(results)
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)



