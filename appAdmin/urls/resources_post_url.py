from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from appAdmin.views import resources_post_view

app_name = "appAdmin"

urlpatterns = (
    [
        path(
            "resources-post/",
            resources_post_view.admin_resources_post,
            name="display-resources-post",
        ),
        path(
            "new-resources-post/",
            resources_post_view.admin_add_resources_post,
            name="add-resources-post",
        ),
        path(
            "update-resources-post/<str:slug>/",
            resources_post_view.admin_edit_resources_post,
            name="update-resources-post",
        ),
        path(
            "delete-resources-post/<str:slug>/",
            resources_post_view.admin_delete_resources_post,
            name="delete-resources-post",
        ),
        path(
            "view-resource-modal/<str:slug>/",
            resources_post_view.view_resource_modal,
            name="view-resource-modal",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
