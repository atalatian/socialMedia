import json
from django.contrib import messages
from django.shortcuts import HttpResponse, get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView, FormMixin
from django.core.exceptions import PermissionDenied, NON_FIELD_ERRORS
from .forms import PostForm, SearchForm, UserForm, PostCommentForm
from .models import Post, User, UserJoin, Comment, Like
from .helpers import authentication, followManager


# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse_lazy('logIn'))


class UserCreate(CreateView):
    model = User
    form_class = UserForm
    template_name = 'socialMediaApp/signUp.html'

    def get_success_url(self):
        authentication.setState(True, self.object.id)
        return reverse_lazy('profile', args=(self.object.id,))

    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data['email'])
            form.add_error('email', error="This username is taken.")
            return super().form_invalid(form)
        except User.DoesNotExist:
            return super().form_valid(form)


class UserDetail(DetailView, FormMixin):
    model = User
    template_name = 'socialMediaApp/profile.html'
    pk_url_kwarg = 'pk'
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        if authentication.getState()['loggedIn'] and authentication.getState()['pk'] == self.kwargs['pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.myObjects.get_posts_by_user_pk(self.kwargs['pk'])
        context['followedUsers'] = UserJoin.objects.filter(user_id=self.kwargs['pk'])
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
    pk_url_kwarg = 'pk'
    template_name = 'socialMediaApp/viewProfile.html'

    def check_if_user_is_followed(self, context):
        try:
            recordedJoin = UserJoin.get_users_by_both(self.kwargs['foreignUser_pk'], self.kwargs['pk'])
            followText = 'Undo Follow'
        except UserJoin.DoesNotExist:
            followText = 'Follow'
        context['followText'] = followText

    def get(self, request, *args, **kwargs):
        if authentication.getState()['loggedIn'] and authentication.getState()['pk'] == self.kwargs['foreignUser_pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.myObjects.get_posts_by_user_pk(self.kwargs['pk'])
        context['foreignUser_pk'] = self.kwargs['foreignUser_pk']
        context['followedUsers'] = \
            UserJoin.get_users_by_user_pk(self.kwargs['pk'])
        self.check_if_user_is_followed(context)
        return context


class UserEnter(FormView):
    model = User
    form_class = UserForm
    template_name = 'socialMediaApp/LogIn.html'

    def form_valid(self, form):
        user = get_object_or_404(User, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        self.success_url = reverse_lazy('profile', args=(user.pk,))
        authentication.setState(True, user.pk)
        return super().form_valid(form)


class PostCreate(FormView):
    model = Post
    form_class = PostForm
    template_name = 'socialMediaApp/createPost.html'

    def get(self, request, *args, **kwargs):
        if authentication.getState()['loggedIn'] and authentication.getState()['pk'] == self.kwargs['pk']:
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
    pk_url_kwarg = 'post_pk'

    def get(self, request, *args, **kwargs):
        if authentication.getState()['loggedIn'] and authentication.getState()['pk'] == self.kwargs['pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['post_pk'])
        return context


class ViewPostDetail(DetailView, FormMixin):
    model = Post
    template_name = 'socialMediaApp/viewPostDetail.html'
    pk_url_kwarg = 'post_pk'
    form_class = PostCommentForm

    @staticmethod
    def assert_user_follow(user_pk, following_pk):
        join = UserJoin.objects.filter(user_id=user_pk, following_id=following_pk)
        if join.exists():
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        if authentication.getState()['loggedIn'] and \
                authentication.getState()['pk'] == self.kwargs['foreignUser_pk']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy("logIn"))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if self.assert_user_follow(self.kwargs['foreignUser_pk'], self.kwargs['pk']):
                comment = Comment(user_id=self.kwargs['foreignUser_pk'],
                                  post_id=self.kwargs['post_pk'],
                                  body=form.cleaned_data['body'])
                comment.save()
                return HttpResponseRedirect(reverse_lazy("viewPostDetail", kwargs={
                    'foreignUser_pk': self.kwargs['foreignUser_pk'],
                    'pk': self.kwargs['pk'],
                    'post_pk': self.kwargs['post_pk'],
                }))
            else:
                raise PermissionDenied
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foreignUser_pk'] = self.kwargs['foreignUser_pk']
        context['user'] = User.objects.get(pk=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['post_pk'])
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


class UserFollow(RedirectView):
    query_string = True
    pattern_name = 'viewProfile'

    def get_redirect_url(self, *args, **kwargs):
        if self.kwargs['foreignUser_pk'] == self.kwargs['pk']:
            raise PermissionDenied
        else:
            followManager.user_follow(self.kwargs['foreignUser_pk'], self.kwargs['pk'])
            try:
                recordedJoin = UserJoin.objects.get(user_id=self.kwargs['foreignUser_pk'],
                                                    following_id=self.kwargs['pk'])
                recordedJoin.delete()
            except UserJoin.DoesNotExist:
                join = UserJoin(user_id=self.kwargs['foreignUser_pk'],
                                following_id=self.kwargs['pk'])
                join.save()
            return super().get_redirect_url(*args, **kwargs)


class UserLike(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        likingUser = User.objects.get(pk=self.kwargs['user_pk'])
        likingUserFollowing = UserJoin.objects.filter(user=likingUser)
        for user in likingUserFollowing:
            if post.user.pk == user.following.pk:
                self.url = self.request.META.get('HTTP_REFERER')
                if not post.user_can_like(likingUser):
                    like = Like(user_id=self.kwargs['user_pk'],
                                post_id=self.kwargs['post_pk'])
                    like.save()
                else:
                    like = Like.objects.get(user_id=self.kwargs['user_pk'],
                                            post_id=self.kwargs['post_pk'])
                    like.delete()
                return super().get_redirect_url(*args, **kwargs)
        raise PermissionDenied
