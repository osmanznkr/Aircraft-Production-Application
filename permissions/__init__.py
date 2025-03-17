from rest_framework import exceptions
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s',
                '%(app_label)s.show_%(model_name)s',
                ],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s',
                 ],
        'PUT': ['%(app_label)s.change_%(model_name)s',
                ],
        'PATCH': ['%(app_label)s.change_%(model_name)s',
                  ],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def get_required_permissions(self, method, perm_slug):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        app, model = perm_slug.split(".")

        kwargs = {
            'app_label': app,
            'model_name': model.lower()
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)
        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        perms = self.get_required_permissions(
            method=request.method, perm_slug=view.perm_slug
        )
        for perm in perms:
            try:
                if request.user.has_perm(perm):
                    return True
            except AttributeError:
                return False
        return False