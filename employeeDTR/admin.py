from django.contrib import admin
from .models import Employee, Department, Position, DTR, LoansTaxes, Deductions, Benefits
from employeeDTR.pyzk.register_biometric import register_fingerprint

class DeductionsInline(admin.TabularInline):
    model = Deductions

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [DeductionsInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        uid = int(obj.id)  
        name = obj.first_name
        print('Django admin TRIGGERED')
        register_fingerprint(uid, name, '123')

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(DTR)
admin.site.register(LoansTaxes)
admin.site.register(Deductions)
admin.site.register(Benefits)