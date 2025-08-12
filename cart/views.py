from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Cart


class CartDetailView(generic.DetailView):
    template_name = 'cart/cart_detail.html'
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return get_object_or_404(Cart, user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            session_key = self.request.session_key
            return get_object_or_404(Cart, session_key=session_key)
