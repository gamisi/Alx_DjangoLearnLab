from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Post, Comment
from django.http import HttpResponse
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

def home(request):
    return render(request, 'blog/home.html')

@login_required
def posts(request):
    return render(request, 'blog/home.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            return Post.objects.filter(tags__name=tag_name)
        return Post.objects.all()

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['tag_slug'])

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Pass the post's comments to the template"""
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object) 
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']

    # Automatically set the author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # Redirect to the list of posts after creating a post
    success_url = reverse_lazy('post_list')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']

    # Ensure the user can only edit their own posts
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    # Ensure only the post author can edit
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Template to confirm post deletion

    # Ensure the user can only delete their own posts
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def test_func(self):
        post = self.get_object()  # Get the post being deleted
        return post.author == self.request.user  # Only allow the author to delete the post

    def get_success_url(self):
        return reverse_lazy('post_list')
  
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        """ Associate the comment with the correct post """
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """ Pass the `post` object to the template """
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Allows only the comment author to edit their comment """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    def test_func(self):
        """ Restrict edit access to only the comment author """
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to edit this comment.")
        return redirect('post_detail', post_id=self.get_object().post.id)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().post.id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Allows only the comment author to delete their comment """
    model = Comment
    template_name = 'blog/confirm_delete_comment.html'

    def test_func(self):
        """ Restrict delete access to only the comment author """
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to delete this comment.")
        return redirect('post_detail', post_id=self.get_object().post.id)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().post.id})

def search_posts(request):
    # Get search query from the request
    query = request.GET.get('q')  
    results = Post.objects.all()

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |  # Search in title
            Q(content__icontains=query) |  # Search in content
            Q(tags__name__icontains=query)  # Search in tags
        ).distinct()

    return render(request, 'blog/search_results.html', {'query': query, 'results': results})