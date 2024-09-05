from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy


def only_host(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'HOST':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('user:profile'))
    return _wrapped_view