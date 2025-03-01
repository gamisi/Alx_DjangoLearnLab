from django.contrib import admin
from .models import Author, Librarian, Library, Book
from django.contrib.auth.models import User
from .models import UserProfile


# Customizing the UserAdmin to display UserProfile role in the user list
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

# Extending UserAdmin to include the UserProfile data in the user list
class CustomUserAdmin(admin.ModelAdmin):
    # Include role field from UserProfile in the user list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'profile__role')  # Filter by UserProfile role

    # Method to get the role from the associated UserProfile
    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'No profile'

    get_role.admin_order_field = 'userprofile__role'  # Allows sorting by role in admin list view
    get_role.short_description = 'Role'  # Column header

    # Adding the UserProfile inline form to User admin
    inlines = [UserProfileInline]

"""
# Register UserProfile in the admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Shows the username and the role in the list view
    search_fields = ('user__username',)  # Allows searching by username
    list_filter = ('role',)  # Filter profiles by role
    ordering = ('user',)  # Orders the list by username

    # Optionally, include inlines to show the UserProfile in the User form
    def get_inline_instances(self, request, obj=None):
        if obj:  # Show the UserProfile inline when editing a User
            from django.contrib.auth.admin import UserAdmin
            inlines = super().get_inline_instances(request, obj)
            inlines.append(UserProfileInline)  # Adding UserProfile inline
            return inlines
        return []"""

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.has_perm('relationship_app.can_add_book')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('relationship_app.can_change_book')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('relationship_app.can_delete_book')
    
    list_display = ("title","author")
    search_fields =("title","author")

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("name","library")
    search_fields =("name,library",)

class LibraryAdmin(admin.ModelAdmin):
    def books_list(self, obj):
        return ", ".join([book.title for book in obj.books.all()])

    list_display = ("name","books_list")
    search_fields = ("name","books_list")

# Register your models here.

# Unregister the default User model and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register UserProfile in the admin interface
admin.site.register(UserProfile)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Book, BookAdmin)
