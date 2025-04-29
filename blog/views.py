from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['comments'] = self.object.comments.all().order_by('-created_at')
       context['comment_form'] = CommentForm()
       return context

class PostCreateView(CreateView):  # Removed LoginRequiredMixin
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'category', 'image', 'author']  # add 'author' if it's a CharField

    def form_valid(self, form):
        # If author is a CharField, the form will provide it; otherwise, set a default
        # form.instance.author = "Anonymous"  # Uncomment if you want to set a default
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

class PostUpdateView(UpdateView):  # Removed LoginRequiredMixin
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'category', 'image']

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

class PostDeleteView(DeleteView):  # Removed LoginRequiredMixin
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:home')  # Update this line

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully!")
    return redirect('blog:post_detail', pk=post.pk)
