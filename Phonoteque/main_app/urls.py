from django.urls import path

from Phonoteque.main_app.views import view_dashboard, IndexListView, find_album_by_url

urlpatterns = [
    path('', IndexListView.as_view(), name="index_page"),
    path('dashboard/', view_dashboard, name="dashboard"),
    path('find_album_by_url', find_album_by_url, name='find_album_by_url')
    # path('find_album/', search_album_view, name='search_form_page'),

    # path('photo/details/<int:pk>/', photo_details, name="pet photo details"),
    # path('photo/like/<int:pk>/', like_pet_photo, name="like pet photo"),
    # path('photo/add/', add_pet_photo, name="add pet photo"),
    # path('photo/edit/<int:pk>/ ', edit_pet_photo, name="edit pet photo"),
    # path('photo/delete/<int:pk>/ ', delete_pet_photo, name="delete pet photo"),

    # path('pet/add/', add_pet, name="add pet"),
    # path('pet/edit/<int:pk>/', edit_pet, name="edit pet"),
    # path('pet/delete/<int:pk>/', delete_pet, name="delete pet"),

]
