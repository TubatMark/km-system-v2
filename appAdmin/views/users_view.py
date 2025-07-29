from appAccounts.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
from utils.user_control import user_access_required
from appAccounts.forms import CustomUserCreationForm
import logging

# Set up logging for better error tracking
logger = logging.getLogger(__name__)


@user_access_required("admin")
def display_users(request):
    users = CustomUser.objects.all()
    total_gen_user = users.filter(user_type="general")
    total_cmi_user = users.filter(user_type="cmi")
    total_secre_user = users.filter(user_type="secretariat")

    # Always pass a form for adding users
    form = CustomUserCreationForm()

    context = {
        "users": users,
        "total_gen_user": total_gen_user,
        "total_cmi_user": total_cmi_user,
        "total_secre_user": total_secre_user,
        "form": form,  # Add form to context
    }
    return render(request, "pages/users.html", context)


@user_access_required("admin")
def admin_add_user(request):
    """
    Enhanced admin function to create new users with comprehensive error handling.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        # Debug: Log the POST data (remove in production)
        logger.debug(f"POST data received: {request.POST}")

        if form.is_valid():
            try:
                # Save using the form's built-in validation and password hashing
                user = form.save(commit=False)

                # Admin-specific modifications
                user.is_active = True
                user.note = "admin created account"

                # Save the user
                user.save()

                logger.info(f"Admin created user: {user.email}")

                # Success message
                messages.success(
                    request,
                    f"User '{user.first_name} {user.last_name}' ({user.email}) has been successfully created and activated.",
                )

                return redirect("appAdmin:display-users")

            except Exception as e:
                logger.error(f"Error saving user: {str(e)}")
                messages.error(request, f"Error creating user: {str(e)}")

        else:
            # Form validation failed
            logger.warning(f"Form validation failed: {form.errors}")

            # Add user-friendly error messages
            messages.error(request, "Please correct the following errors:")

            # Process field errors
            for field_name, error_list in form.errors.items():
                # Get human-readable field name
                if field_name in form.fields:
                    field_label = (
                        form.fields[field_name].label
                        or field_name.replace("_", " ").title()
                    )
                else:
                    field_label = field_name.replace("_", " ").title()

                for error in error_list:
                    messages.error(request, f"{field_label}: {error}")

            # Process non-field errors
            for error in form.non_field_errors():
                messages.error(request, str(error))

        # Get all users for the display (same as display_users view)
        users = CustomUser.objects.all()
        total_gen_user = users.filter(user_type="general")
        total_cmi_user = users.filter(user_type="cmi")
        total_secre_user = users.filter(user_type="secretariat")

        # Return form with data, errors, and all context needed for the template
        context = {
            "users": users,
            "total_gen_user": total_gen_user,
            "total_cmi_user": total_cmi_user,
            "total_secre_user": total_secre_user,
            "form": form,  # This form contains the validation errors and submitted data
        }
        return render(request, "pages/users.html", context)

    else:
        # GET request - redirect to display_users instead
        return redirect("appAdmin:display-users")


# Alternative: Combine both views into one
@user_access_required("admin")
def manage_users(request):
    """
    Combined view to display users and handle user creation.
    """
    # Get all users for display
    users = CustomUser.objects.all()
    total_gen_user = users.filter(user_type="general")
    total_cmi_user = users.filter(user_type="cmi")
    total_secre_user = users.filter(user_type="secretariat")

    # Handle form submission
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        logger.debug(f"POST data received: {request.POST}")

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = True
                user.note = "admin created account"
                user.save()

                logger.info(f"Admin created user: {user.email}")

                messages.success(
                    request,
                    f"User '{user.first_name} {user.last_name}' ({user.email}) has been successfully created and activated.",
                )

                # Redirect to avoid re-submission on refresh
                return redirect("appAdmin:manage-users")

            except Exception as e:
                logger.error(f"Error saving user: {str(e)}")
                messages.error(request, f"Error creating user: {str(e)}")
        else:
            # Form validation failed
            logger.warning(f"Form validation failed: {form.errors}")

            messages.error(request, "Please correct the following errors:")

            for field_name, error_list in form.errors.items():
                if field_name in form.fields:
                    field_label = (
                        form.fields[field_name].label
                        or field_name.replace("_", " ").title()
                    )
                else:
                    field_label = field_name.replace("_", " ").title()

                for error in error_list:
                    messages.error(request, f"{field_label}: {error}")

            for error in form.non_field_errors():
                messages.error(request, str(error))
    else:
        # GET request - create empty form
        form = CustomUserCreationForm()

    context = {
        "users": users,
        "total_gen_user": total_gen_user,
        "total_cmi_user": total_cmi_user,
        "total_secre_user": total_secre_user,
        "form": form,
    }

    return render(request, "pages/users.html", context)
