from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from .models import Profile

from Phonotheque.accounts_app.forms import UserRegistrationForm, UserEditForm, ProfileEditForm, UserAndProfileDeleteForm


def register_user_create_profile(request):
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

                # Create the user profile as well by just copying newly created user's data
                new_profile = Profile.objects.create(user=new_user)

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
def edit_user_and_profile(request, pk):
    user_instance = User.objects.get(pk=pk)
    profile_instance = Profile.objects.get(pk=pk)

    # check if logged-in user is user whose profile will be edited OR staff
    if user_instance != request.user and not request.user.is_staff:
        messages.add_message(request, messages.INFO, 'Yo! Are you trying to edit someone else\'s profile? Tut-tut...')
        return redirect('profiles-list')

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user_instance)
        profile_form = ProfileEditForm(request.POST, instance=profile_instance)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.INFO, 'Profile updated successfully.')
            return redirect('profile-details', pk)

    else:  # if GET
        user_form = UserEditForm(instance=user_instance)

        # RelatedObjectDoesNotExist at /accounts/edit/ User has no profile.
        # It happens if user is created via admin panel, i.e. first superuser
        try:
            profile_form = ProfileEditForm(instance=profile_instance)
        except Profile.DoesNotExist:
            profile_form = ProfileEditForm(instance=user_instance)

        profile_instance = Profile.objects.get(pk=pk)

    return render(request,
                  'registration/profile_edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'current_profile': profile_instance})


@login_required
def delete_user_and_profile(request, pk):
    instance = User.objects.get(pk=pk)

    if instance != request.user \
            and not request.user.has_perm('accounts_app.delete_profile'):  # accounts_app|profile|Can delete profile
        # Verification if staff user has permission to delete users will be carried out in the template, button won't show if not
        messages.add_message(request, messages.INFO,
                             f'Ooopsy! User {instance.username} won\'t be happy if you delete their account.\n'
                             f'Luckily you can\'t do it.')
        return redirect('profiles-list')

    if request.method == 'POST':
        form = UserAndProfileDeleteForm(request.POST, instance=instance)
        form.save()  # save method is overwritten in form
        messages.add_message(request, messages.INFO, 'Profile deleted successfully.\nSad to see you go by the way...')
        return redirect('index_page')

    else:
        form = UserAndProfileDeleteForm(instance=instance)

    return render(request,
                  'registration/delete_user_and_profile.html',
                  {'form': form,
                   'current_profile': Profile.objects.get(pk=instance.pk)})


@login_required()
def deactivate_or_reactivate_user(request, user_pk):
    user_to_edit = User.objects.get(pk=user_pk)
    if request.user.is_staff:
        user_to_edit.is_active = not user_to_edit.is_active
        user_to_edit.save()
        messages.add_message(request, messages.INFO,
                             f'Profile of {user_to_edit.username} disabled successfully by {request.user.username}')
        return redirect('profiles-list')
    else:
        messages.add_message(request, messages.INFO,
                             f'You have no permissions to deactivate the profile of {user_to_edit.username}')
        return redirect('profiles-list')


class UserLoginView(auth_views.LoginView):
    success_url = 'dashboard'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (field_name, field) in self.form_class.base_fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = f"Enter {field_name.title()}"


class UserLogoutView(auth_views.LogoutView):
    next_page = 'index_page'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'You have successfully logged out from your account.')
        messages.add_message(request, messages.INFO, 'You can either close this tab or Sign In again.')
        return response


class ProfileListView(views.ListView, LoginRequiredMixin):
    model = Profile
    template_name = 'registration/profile_list.html'

    '''
    We can have a scenario if an admin disables their own account, then
    context['current_profile'] = Profile.objects.get(user_id=self.request.user.pk)
    (see get_context_data() below)
    will raise an Exception because apparently profile cannot be created from an inactive user
    '''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active:
            return redirect(reverse_lazy('index_page'))

        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data()

        '''
        superuser raises DoesNotExist at /accounts/profiles/ as they are created with createsuperuser in manage.py
        hence are not assigned a profile automatically => if ObjectDoesNotExist exception, create profile for them here
        '''
        try:
            context['current_profile'] = Profile.objects.get(user_id=self.request.user.pk)
        except ObjectDoesNotExist:
            Profile.objects.create(user=self.request.user)
            context['current_profile'] = Profile.objects.get(user_id=self.request.user.pk)

        # get all other users' profiles apart from current user
        # Originally regular users were not meant to be able to view staff profiles, this has been amended below
        regular_users = User.objects \
            .filter(is_superuser=False, is_staff=False) \
            .exclude(pk=self.request.user.pk)
        # pipe is OR
        staff_users = User.objects.filter(is_superuser=True) |  \
            User.objects.filter(is_staff=True) \
            .exclude(pk=self.request.user.pk)
        
        context['non_staff_profiles'] = Profile.objects.filter(user__in=regular_users)
        context['staff_profiles'] = Profile.objects.filter(user__in=staff_users)
        context['all_profiles'] = context['non_staff_profiles'] + context['staff_profiles']

        return context


class ProfileDetailView(views.DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'registration/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        searched_user = User.objects.get(pk=self.object.pk)
        if searched_user.is_active or self.request.user.is_staff:
            context['searched_user'] = searched_user
        else:
            context['searched_user'] = None
        return context


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (field_name, field) in self.form_class.base_fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = f"Enter {field_name.title()}"
