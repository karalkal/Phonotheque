from django.urls import path

from Phonoteque.main_app.views import view_dashboard, search_album_view, IndexListView

urlpatterns = [
    path('', IndexListView.as_view(), name="index_page"),
    path('dashboard/', view_dashboard, name="dashboard"),

    # path('profile/', profile_details, name="profile"),
    # path('profile/create/', create_profile_view, name="create profile"),
    # path('profile/edit/', edit_profile_view, name="edit profile"),
    # path('profile/delete/', delete_profile_view, name="delete profile"),

    path('find_album/', search_album_view, name='search_form_page'),

    # path('photo/details/<int:pk>/', photo_details, name="pet photo details"),
    # path('photo/like/<int:pk>/', like_pet_photo, name="like pet photo"),
    # path('photo/add/', add_pet_photo, name="add pet photo"),
    # path('photo/edit/<int:pk>/ ', edit_pet_photo, name="edit pet photo"),
    # path('photo/delete/<int:pk>/ ', delete_pet_photo, name="delete pet photo"),

    # path('pet/add/', add_pet, name="add pet"),
    # path('pet/edit/<int:pk>/', edit_pet, name="edit pet"),
    # path('pet/delete/<int:pk>/', delete_pet, name="delete pet"),

]
