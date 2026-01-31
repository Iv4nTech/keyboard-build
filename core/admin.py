from django.contrib import admin
from .models import Case, Component, GetLevel, Keyboard, KeyboardComponent, Keycaps, Level, Pcb, Plate, SocialNetwork, SocialNetworkUser, Switch, User
from django.contrib.auth.admin import UserAdmin

class UserLevelIntermediate(admin.StackedInline):
    model = GetLevel
    extra = 1

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image','bio')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('image','bio')}),
    )

    inlines = [UserLevelIntermediate]


admin.site.register(Case)
admin.site.register(Component)
admin.site.register(GetLevel)
admin.site.register(Keyboard)
admin.site.register(KeyboardComponent)
admin.site.register(Keycaps)
admin.site.register(Level)
admin.site.register(Pcb)
admin.site.register(Plate)
admin.site.register(SocialNetwork)
admin.site.register(SocialNetworkUser)
admin.site.register(Switch)
admin.site.register(User, CustomUserAdmin)