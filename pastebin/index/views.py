from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from pastebin.models import Paste

class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

@login_required
def account_profile(request):
    pass

class ListView(LoginRequiredMixin, generic.ListView):
    template_name = 'index/pastes/list.html'
    context_object_name = 'pastes_list'

    def get_queryset(self):
        return Paste.objects.filter(author=self.request.user).order_by('-created')

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Paste
    template_name = 'index/pastes/show.html'

    def get_object(self):
        return get_object_or_404(Paste, hash=self.kwargs['hash'], author=self.request.user)