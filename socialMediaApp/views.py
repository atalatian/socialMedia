import json

from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponse, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView, FormMixin

from .forms import PostForm, SearchForm, UserSignUpForm, PostCommentForm, UserUpdateForm, UserEnterForm
from .models import Post, User, UserJoin, Comment, Like
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as DjangoUser


# Create your views here.
def index(request):
    return HttpResponse("Successful")


class UserSignUp(FormView):
    model = User
    form_class = UserSignUpForm
    template_name = 'socialMediaApp/signUp.html'

    def form_valid(self, form):
        user = DjangoUser.objects.create_user(username=form.cleaned_data['email'],
                                              email=form.cleaned_data['email'],
                                              password=form.cleaned_data['password'])
        user.save()
        form.save()
        user_pk = User.objects.get(email=form.cleaned_data['email']).pk
        user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(self.request, user)
        self.success_url = reverse_lazy('profile', kwargs={"pk": user_pk})
        return super().form_valid(form)


class UserUpdate(FormView):
    model = User
    form_class = UserUpdateForm
    template_name = 'socialMediaApp/updateProfile.html'

    def get_initial(self):
        user = User.objects.get(pk=self.kwargs['pk'])
        initial_dict = {
            'password': user.password,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'gender': user.gender,
            'bio': user.bio,
            'website': user.website,
        }
        return initial_dict

    def form_valid(self, form):
        user = User.objects.get(pk=self.kwargs['pk'])
        djangoUser = DjangoUser.objects.get(username=user.email)
        djangoUser.set_password(form.cleaned_data['password'])
        djangoUser.save()
        user.password = form.cleaned_data['password'] or user.password
        user.firstName = form.cleaned_data['firstName']
        user.lastName = form.cleaned_data['lastName']
        user.gender = form.cleaned_data['gender']
        user.bio = form.cleaned_data['bio']
        user.website = form.cleaned_data['website']
        user.save()
        self.success_url = reverse_lazy('profile', kwargs={"pk": self.kwargs['pk']})
        return super(UserUpdate, self).form_valid(form)


class UserDetail(DetailView, FormMixin):
    model = User
    template_name = 'socialMediaApp/profile.html'
    pk_url_kwarg = 'pk'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(user_id=self.kwargs['pk'])
        context['followedUsers'] = UserJoin.objects.filter(user_id=self.kwargs['pk'], accept=True)
        context['userFollowers'] = UserJoin.objects.filter(following_id=self.kwargs['pk'], accept=True)
        context['requested'] = UserJoin.objects.filter(following_id=self.kwargs['pk'], accept=False)
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
            recordedJoin = UserJoin.objects.get(user_id=self.kwargs['foreignUser_pk'],
                                                following_id=self.kwargs['pk'])
            if recordedJoin.accept:
                followText = 'Undo Follow'
            else:
                followText = 'Requested'
        except UserJoin.DoesNotExist:
            followText = 'Follow'
        context['followText'] = followText

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(user_id=self.kwargs['pk'])
        context['foreignUser_pk'] = self.kwargs['foreignUser_pk']
        context['followedUsers'] = UserJoin.objects.filter(user_id=self.kwargs['pk'], accept=True)
        context['userFollowers'] = UserJoin.objects.filter(following_id=self.kwargs['pk'], accept=True)
        self.check_if_user_is_followed(context)
        return context


class UserEnter(FormView):
    model = User
    form_class = UserEnterForm
    template_name = 'socialMediaApp/LogIn.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user_pk = get_object_or_404(User, email=form.cleaned_data['email'], password=form.cleaned_data['password']).pk
        user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(self.request, user)
        self.success_url = reverse_lazy('profile', kwargs={'pk': user_pk})
        return super(UserEnter, self).form_valid(form)


class PostCreate(FormView):
    model = Post
    form_class = PostForm
    template_name = 'socialMediaApp/createPost.html'

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
            try:
                recordedJoin = UserJoin.objects.get(user_id=self.kwargs['foreignUser_pk'],
                                                    following_id=self.kwargs['pk'])
                if recordedJoin.accept:
                    recordedJoin.delete()
            except UserJoin.DoesNotExist:
                join = UserJoin(user_id=self.kwargs['foreignUser_pk'],
                                following_id=self.kwargs['pk'], accept=False)
                join.save()
            return super().get_redirect_url(*args, **kwargs)


class UserRequest(RedirectView):
    query_string = True
    pattern_name = 'profile'


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
