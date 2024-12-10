"""
Views which allow users to create and activate accounts.

"""

from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import  reverse_lazy,reverse
from registration.forms import ResendActivationForm,Profile
from registration.models import Profile
from  .forms import UpdateForm
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.utils.timezone import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

REGISTRATION_FORM_PATH = getattr(
    settings, "REGISTRATION_FORM", "registration.forms.RegistrationForm"
)
REGISTRATION_FORM = import_string(REGISTRATION_FORM_PATH)
ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = getattr(
    settings, "ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS", True
)


class RegistrationView(FormView):
    """
    Base class for user registration views.

    """

    disallowed_url = "registration_disallowed"
    form_class = REGISTRATION_FORM
    http_method_names = ["get", "post", "head", "options", "trace"]
    success_url = None
    template_name = "registration/registration_form.html"

    @method_decorator(sensitive_post_parameters("password1", "password2"))
    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed and if user is logged in before even bothering to
        dispatch or do other processing.

        """
        if ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS:
            if self.request.user.is_authenticated:
                if settings.LOGIN_REDIRECT_URL is not None:
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    raise Exception(
                        (
                            "You must set a URL with LOGIN_REDIRECT_URL in "
                            "settings.py or set "
                            "ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS=False"
                        )
                    )

        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(form)
        success_url = self.get_success_url(new_user)

        if hasattr(self.request, "session"):
            self.request.session["registration_email"] = form.cleaned_data[
                "email"
            ]

        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return True

    def register(self, form):
        """
        Implement user-registration logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user=None):
        """
        Use the new user when constructing success_url.

        """
        return super().get_success_url()


class ActivationView(TemplateView):
    """
    Base class for user activation views.

    """

    http_method_names = ["get"]
    template_name = "registration/activate.html"

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def activate(self, *args, **kwargs):
        """
        Implement account-activation logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


class ResendActivationView(FormView):
    """
    Base class for resending activation views.
    """

    form_class = ResendActivationForm
    template_name = "registration/resend_activation_form.html"

    def form_valid(self, form):
        """
        Regardless if resend_activation is successful, display the same
        confirmation template.

        """
        self.resend_activation(form)
        return self.render_form_submitted_template(form)

    def resend_activation(self, form):
        """
        Implement resend activation key logic here.
        """
        raise NotImplementedError

    def render_form_submitted_template(self, form):
        """
        Implement rendering of confirmation template here.

        """
        raise NotImplementedError


class ApprovalView(TemplateView):

    http_method_names = ["get"]
    template_name = "registration/admin_approve.html"

    def get(self, request, *args, **kwargs):
        approved_user = self.approve(*args, **kwargs)
        if approved_user:
            success_url = self.get_success_url(approved_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def approve(self, *args, **kwargs):
        """
        Implement admin-approval logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


class ProfileView(TemplateView):
    template_name = "profiles/home.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['title'] = "My Profile"
        context['year'] = datetime.now().year
        context['details'] = User.objects.filter(username=self.request.user)
        try:
            context['user_profile'] = Profile.objects.filter(user_id=self.request.user.pk)
        except Profile.DoesNotExist:
            context['user_profile'] = ''
        return context


class CreateProfileView(TemplateView):
    template_name = "profiles/create_profile.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProfileView, self).get_context_data(**kwargs)
        context['title'] = 'Create Profile'
        context['form'] = UpdateForm()
        return context

    def post(self, request, *args, **kwargs):
        profile_form = UpdateForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if profile_form.is_valid():
            profile, created = Profile.objects.get_or_create(user=request.user)
            for field, value in profile_form.cleaned_data.items():
                if field == 'profile_image' and not value:
                    continue  # Skip updating profile_image if no new file is provided
                setattr(profile, field, value)
            profile.save()
            return redirect('profiles:profile_home')  # Ensure you have the correct redirect URL
        else:
            return render(request, self.template_name, {'form': profile_form})


class UpdateProfileView(UpdateView):
    form_class = UpdateForm
    model = Profile
    template_name = "profiles/update.html"  # Ensure this template path is correct
    success_url = reverse_lazy('registration:profile_update')  # Adjust the success URL as needed

    def get_context_data(self, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        context['title'] = 'Update Profile'
        context['year'] = datetime.now().year
        try:
            context['profile'] = Profile.objects.get(user=self.request.user)  # Use get() for a single object
        except Profile.DoesNotExist:
            context['profile'] = None
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.user.name = profile.name
        profile.user.last_name = profile.surname
        profile.user.save()
        profile.save()
        return super(UpdateProfileView, self).form_valid(form)





