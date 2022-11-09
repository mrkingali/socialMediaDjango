from django.shortcuts import render,redirect
from django.views import View
from .models import Post
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import  messages
from django.utils.text import slugify
from .forms import PostCreateUpdateForm



class HomeView(View):
    def get(self,request):
        posts=Post.objects.all()
        return render(request,'home/index.html',{'posts':posts})
    def post(self,request):
        return render(request,'home/index.html')




class PostDetailView(View):
    def get(self,request,post_id,post_slug):
        post=Post.objects.get(pk=post_id,slug=post_slug)
        comments = post.post_comment.filter(is_reply=False)
        return render(request, 'home/post_detail.html', {'post': post, 'comments': comments})


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




