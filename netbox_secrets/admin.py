from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.shortcuts import redirect, render

from .forms import ActivateUserKeyForm
from .models import UserKey


@admin.register(UserKey)
class UserKeyAdmin(admin.ModelAdmin):
    actions = ['activate_selected']
    list_display = ['user', 'is_filled', 'is_active', 'created']
    fields = ['user', 'public_key', 'is_active', 'last_updated']
    readonly_fields = ['user', 'is_active', 'last_updated']

    def has_add_permission(self, request):
        # Don't allow a user to create a new public key directly.
        return False

    def has_delete_permission(self, request, obj=None):
        # Don't allow a user to delete a public key directly.
        return False

    def get_readonly_fields(self, request, obj=None):
        # Don't allow a user to modify an existing public key directly.
        if obj and obj.public_key:
            return ['public_key'] + self.readonly_fields
        return self.readonly_fields

    def response_action(self, request, queryset):
        # Modify request.POST to remove the empty string from the list of selected objects.
        post = request.POST.copy()
        post.setlist(ACTION_CHECKBOX_NAME, list(filter(None, post.getlist(ACTION_CHECKBOX_NAME))))
        request.POST = post

        return super().response_action(request, queryset)

    @admin.action(description='Activate selected public keys', permissions=['change'])
    def activate_selected(self, request, queryset):
        """
        Enable bulk activation of UserKeys
        """
        try:
            my_userkey = UserKey.objects.get(user=request.user)
        except UserKey.DoesNotExist:
            messages.error(request, "You do not have an active User Key.")
            return redirect('admin:netbox_secrets_userkey_changelist')

        if 'activate' in request.POST:
            form = ActivateUserKeyForm(request.POST)
            if form.is_valid():
                master_key = my_userkey.get_master_key(form.cleaned_data['secret_key'])
                if master_key is not None:
                    for uk in form.cleaned_data['_selected_action']:
                        uk.activate(master_key)
                    return redirect('admin:netbox_secrets_userkey_changelist')
                else:
                    messages.error(
                        request,
                        "Invalid private key provided. Unable to retrieve master key.",
                        extra_tags='error',
                    )
        else:
            form = ActivateUserKeyForm(initial={'_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)})

        return render(
            request,
            'netbox_secrets/activate_keys.html',
            {
                'form': form,
            },
        )

