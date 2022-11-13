from django.shortcuts import render,redirect
from django.views import View
from .models import Post,Comment,Like
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import  messages
from django.utils.text import slugify
from .forms import PostCreateUpdateForm,CommentCreateForm,CommentReplyForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


class HomeView(View):
    def get(self,request):
        posts=Post.objects.all()
        return render(request,'home/index.html',{'posts':posts})
    def post(self,request):
        return render(request,'home/index.html')




class PostDetailView(View):
    form_class=CommentCreateForm
    form_class_reply=CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance=get_object_or_404(Post,pk=kwargs['post_id'],slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):

        comments = self.post_instance.post_comment.filter(is_reply=False)

        can_like=False
        self.post_instance.user_can_like(request.user)
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like=True
        return render(request, 'home/post_detail.html', {'post': self.post_instance, 'comments': comments,'form':self.form_class,'replyform':self.form_class_reply ,'can_like':can_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid:
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.post=self.post_instance
            new_comment.save()
            messages.success(request,'your comment successfully added','success')
            return redirect('home:post_detail',self.post_instance.id,self.post_instance.slug)
        messages.error(request, 'your comment successfully added','danger)')

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post=Post.objects.get(pk=post_id)
        if request.user.id==post.user.id:
            post.delete()
            messages.success(request,"post deleted successfully",'success')
        else:
            messages.error(request,"you cant deleet this post" ,'danger')
        return redirect("home:home")


class PostUpdateView(LoginRequiredMixin,View):

    class_form=PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance=Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        post=self.post_instance

        if not request.user.id==post.user.id:
            messages.error(request,"you cant update this post",'danger')
            return redirect("home:home")
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        post=self.post_instance
        form=self.class_form(instance=post)
        return render(request,'home/post_update.html',{'form':form})

    def post(self,request,*args,**kwargs):
        post = self.post_instance
        form = self.class_form(request.POST,instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug=slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request,'post updated sccessfully','success')
            return redirect("home:post_detail",post.id,post.slug)


class PostCreatView(LoginRequiredMixin,View):
    class_form=PostCreateUpdateForm

    def get(self,request,*args,**kwargs):
        form=self.class_form
        return render(request,"home/post_creat.html",{'form':form})

    def post(self,request,*args,**kwargs):
        form=self.class_form(request.POST)

        if form.is_valid():

            newpost=form.save(commit=False)
            newpost.user=request.user
            newpost.slug=slugify(form.cleaned_data['body'][:30])
            newpost.save()
            messages.success(request,"post creat successfully",'success')
            return redirect("account:profile_user",request.user.id)

        messages.error(request,'post cant creat','danger')
        return redirect("account:profile_user",request.user.id)


class CommentReplyView(LoginRequiredMixin,View):
    form_class=CommentReplyForm
    def post(self,request,post_id,comment_id):
        post=get_object_or_404(Post,id=post_id)
        comment=get_object_or_404(Comment,id=comment_id)

        form=self.form_class(request.POST)
        if form.is_valid():
            newform=form.save(commit=False)
            newform.user=request.user
            newform.post=post
            newform.reply=comment
            newform.is_reply=True
            newform.save()
            messages.success(request,'your reply sent successfully','success')
        else:
            messages.error(request,'cant sent your reply','danger')

        return redirect('home:post_detail',post.id,post.slug)

class PostLikeView(LoginRequiredMixin,View):


    def get(self,request,post_id):
        post=get_object_or_404(Post,id=post_id)
        like=Like.objects.filter(post=post,user=request.user)
        if like.exists():
            messages.error(request,"you have already like this post",'danger')
        else:
            Like.objects.create(post=post,user=request.user)
            messages.success(request,'you liked successfully','success')
        return redirect('home:post_detail',post.id,post.slug)