"""
Views for serving frontend templates
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist


class GenericTemplateView(TemplateView):
    """Generic view to serve templates by filename"""
    
    def get_template_names(self):
        filename = self.kwargs.get('filename', '')
        # Ensure the filename has .html extension
        if not filename.endswith('.html'):
            filename += '.html'
        return [filename]
    
    def get(self, request, *args, **kwargs):
        # Check if template exists, otherwise raise 404
        try:
            get_template(self.get_template_names()[0])
        except TemplateDoesNotExist:
            raise Http404("Template not found")
        return super().get(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'index.html'


class Home1View(TemplateView):
    template_name = 'index-1.html'


class Home6View(TemplateView):
    template_name = 'index-6.html'


class ShopView(TemplateView):
    template_name = 'shop.html'


class ShopSidebarView(TemplateView):
    template_name = 'shop-sidebar.html'


class ProductDetailView(TemplateView):
    template_name = 'single-product.html'


class CartView(TemplateView):
    template_name = 'cart.html'


class CheckoutView(TemplateView):
    template_name = 'checkout.html'


class WishlistView(TemplateView):
    template_name = 'wishlist.html'


class MyAccountView(TemplateView):
    template_name = 'my-account.html'


class SignInView(TemplateView):
    template_name = 'sign-in.html'


class SignUpView(TemplateView):
    template_name = 'sign-up.html'


class ForgotPasswordView(TemplateView):
    template_name = 'forgot-password.html'


class ResetPasswordView(TemplateView):
    template_name = 'reset-password.html'


class AboutUsView(TemplateView):
    template_name = 'about-us.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class BlogView(TemplateView):
    template_name = 'blog.html'


class BlogGridView(TemplateView):
    template_name = 'blog-grid.html'


class BlogDetailsView(TemplateView):
    template_name = 'blog-details.html'


class BlogAudioView(TemplateView):
    template_name = 'blog-audio.html'


class BlogVideoView(TemplateView):
    template_name = 'blog-video.html'


class BlogGalleryView(TemplateView):
    template_name = 'blog-gallery.html'


class BlogQuoteView(TemplateView):
    template_name = 'blog-quote.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy-policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'terms-of-service.html'


class ComingSoonView(TemplateView):
    template_name = 'coming-soon.html'


class NotFoundView(TemplateView):
    template_name = '404.html'
