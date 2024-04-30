from django.contrib import admin
from .models import Account, BillingAddress, PaymentMethod

class BillingAddressInline(admin.TabularInline):
    model = Account.BillingAddresses.through
    extra = 1

class PaymentMethodInline(admin.TabularInline):
    model = Account.PaymentMethods.through
    extra = 1

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'phone',
        'is_active',
        'is_admin',
        'is_superuser',
        'is_staff',
        'last_active',
        'registered_on',
    )
    list_filter = ('is_active', 'is_admin', 'is_superuser', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone')
    readonly_fields = ('last_active', 'registered_on')
    ordering = ('-last_active',)
    inlines = [BillingAddressInline, PaymentMethodInline]

class BillingAddressAdmin(admin.ModelAdmin):
    list_display = (
        'billing_address_id',
        'user_id',
        'first_name',
        'last_name',
        'address_line1',
        'city',
        'state',
        'country',
        'postal_code',
        'phone_number',
        'created_at',
        'updated_at',
    )
    search_fields = ('user_id', 'first_name', 'last_name', 'postal_code', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'card_type', 'card_last_four', 'expiration_date')
    search_fields = ('card_type', 'card_last_four')

admin.site.register(Account, AccountAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)