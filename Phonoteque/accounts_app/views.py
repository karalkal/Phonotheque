from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import generic as views

from .models import Profile

from Phonoteque.accounts_app.forms import UserRegistrationForm, UserEditForm, ProfileEditForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            try:  # If validations OK
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the User object
                new_user.save()

                # Create the user profile as well
                new_profile = Profile.objects.create(user=new_user)

                # And copy name(s) to it
                new_profile.first_name = user_form.cleaned_data['first_name']
                if user_form.cleaned_data['last_name']:
                    new_profile.last_name = user_form.cleaned_data['last_name']
                new_profile.save()

                return render(request, 'registration/register_done.html', {'new_user': new_user})

            except Exception as ex:  # If validation fails
                messages.error(request, str(ex))
                return redirect('register')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserEditForm(instance=request.user)

        # RelatedObjectDoesNotExist at /accounts/edit/ User has no profile.
        # It happens if user is created via admin panel, i.e. first superuser
        try:
            profile_form = ProfileEditForm(instance=request.user.profile)
        except Profile.DoesNotExist:
            profile_form = ProfileEditForm(instance=request.user)

        current_profile = Profile.objects.get(pk=request.user.pk)

    return render(request,
                  'registration/profile_edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'current_profile': current_profile})


class UserLoginView(auth_views.LoginView):
    success_url = 'dashboard'

    # def get_success_url(self):
    #     user_pk = self.request.user.pk
    #     return reverse_lazy('dashboard', kwargs={'pk': user_pk})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (field_name, field) in self.form_class.base_fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = f"Enter {field_name.title()}"


class UserLogoutView(auth_views.LogoutView):
    """
    Log out the user and display the 'You are logged out' message.
    """

    next_page = 'index_page'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'You have successfully logged out from your account.')
        messages.add_message(request, messages.INFO, 'You can either close this tab or log in again.')
        return response


class ProfileDetailView(views.DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'registration/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        searched_user = User.objects.get(pk=self.object.pk)
        context['searched_user'] = searched_user
        return context


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (field_name, field) in self.form_class.base_fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = f"Enter {field_name.title()}"
