from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blogapp/home.html', context)


class PostListView(ListView):
    model = Post
    # looks for template with naming structure of <app>/<model>_<viewtype>.html
    # in this case it's looking for blogapp/post_list
    template_name = 'blogapp/home.html'
    # in the template, we are already using the {{ posts }} name to get our posts.
    # by default, Django is looking for one named object_list. we are changing it below.
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


# loginrequiredMixin causes a redirect to the login view if a user attempts to use this page
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title',
        'content'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form=form)


# loginrequiredMixin causes a redirect to the login view if a user attempts to use this page
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = [
        'title',
        'content'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form=form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    context = {

    }
    return render(request, 'blogapp/about.html', {'title': 'About'})
