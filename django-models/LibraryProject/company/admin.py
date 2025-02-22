from django.contrib import admin
from .models import Department, Employee, Product, ProductDescription

# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_name',)
    search_fields = ('dept_name',)
    list_filter = ('dept_name',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_name', 'department')
    search_fields = ('emp_name', 'department')
    list_filter = ('emp_name', 'department')

    def department(self, obj):
        return obj.department.dept_name

class ProductAdmin(admin.ModelAdmin):
    list_display  = ('prod_name',)
    search_fields  = ('prod_name',)
    list_filter  = ('prod_name',)

class ProdDescriptionAdmin(admin.ModelAdmin):
    list_display  = ('product','prod_description')
    search_fields  = ('product','prod_description')
    list_filter  = ('product','prod_description')

    def product(self, obj):
        return obj.product.prod_name


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDescription, ProdDescriptionAdmin)
