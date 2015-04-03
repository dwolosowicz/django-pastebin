from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from pastebin.models import Paste, Syntax
from .forms import PasteForm


class LoginRequiredMixin(object):
    "Mixing serves as a class view version of login_required decorator"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AccountProfileView(LoginRequiredMixin, generic.View):
    template_name = 'registration/account.html'

    def get(self, request):
        return render(request, self.template_name)

class PasteListView(LoginRequiredMixin, generic.ListView):
    template_name = 'index/pastes/list.html'
    context_object_name = 'paste_list'

    def get_queryset(self):
        return Paste.objects.by_author(self.request.user)


class SyntaxesMixin(object):

    def get_context_data(self, **kwargs):
        context = super(SyntaxesMixin, self).get_context_data(**kwargs)

        context['js_syntaxes'] = Syntax.objects.to_json()

        return context


class CreatePasteView(LoginRequiredMixin, SyntaxesMixin, generic.CreateView):
    form_class = PasteForm
    template_name = "index/pastes/form.html"
    success_url = reverse_lazy('pastes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePasteView, self).form_valid(form)


class UpdatePasteView(LoginRequiredMixin, SyntaxesMixin, generic.UpdateView):
    form_class = PasteForm
    template_name = "index/pastes/form.html"
    context_object_name = "paste"
    success_url = reverse_lazy('pastes')

    def get_object(self):
        "Returns Paste matching the currently logged in user and hash"
        paste_hash = self.kwargs['hash']
        author = self.request.user

        return get_object_or_404(Paste, hash=paste_hash, author=author)


class DeletePasteView(LoginRequiredMixin, generic.DeleteView):
    form_class = PasteForm
    template_name = "index/pastes/delete.html"
    context_object_name = "paste"
    success_url = reverse_lazy('pastes')

    def get_object(self):
        "Returns Paste matching the currently logged in user and hash"
        paste_hash = self.kwargs['hash']
        author = self.request.user

        return get_object_or_404(Paste, hash=paste_hash, author=author)


class PasteView(LoginRequiredMixin, generic.DetailView):
    model = Paste
    template_name = 'index/pastes/show.html'

    def get_object(self):
        "Returns Paste matching the currently logged in user and hash"
        paste_hash = self.kwargs['hash']
        author = self.request.user

        return get_object_or_404(Paste, hash=paste_hash, author=author)

    def get_context_data(self, **kwargs):
        context = super(PasteView, self).get_context_data(**kwargs)

        context['paste_list'] = Paste.objects.by_author(self.request.user)[:5]

        return context
