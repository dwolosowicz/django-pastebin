from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic

from pastebin.models import Paste, Syntax  # @UnresolvedImport

from .forms import PasteForm


class LoginRequiredMixin(object):
    "Mixin serves as a class view version of login_required decorator"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class PasteAuthenticationMixin(object):
    'Mixin serves as a protection based on paste visibility'

    def get_object(self):
        o = super(PasteAuthenticationMixin, self).get_object()

        if o.visible_to(Paste.ONLY_SPECIFIED_USERS) and not o.is_allowed(self.request.user):
            raise Http404("Paste doesn't exist")


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

    def get_form_kwargs(self):
        "Injecting the currently logged in user into paste form"
        kwargs = generic.CreateView.get_form_kwargs(self)
        
        kwargs['user'] = self.request.user
        
        return kwargs


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
    
    def get_form_kwargs(self):
        "Injecting the currently logged in user into paste form"
        kwargs = generic.UpdateView.get_form_kwargs(self)
        
        kwargs['user'] = self.request.user
        
        return kwargs


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


class PasteView(PasteAuthenticationMixin, LoginRequiredMixin, generic.DetailView):
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
