from django.contrib import admin
from django import forms
from .models import PedidoCono, TOPPINGS_VALIDOS

class PedidoConoForm(forms.ModelForm):
    # Campo personalizado para toppings
    toppings_seleccionados = forms.MultipleChoiceField(
        choices=[(t, t) for t in TOPPINGS_VALIDOS],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Toppings (selecciona los que quieras)"
    )
    
    class Meta:
        model = PedidoCono
        fields = '__all__'
        widgets = {
            'toppings': forms.HiddenInput(),  # Ocultar el campo JSON
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, mostrar toppings seleccionados
        if self.instance and self.instance.pk:
            self.fields['toppings_seleccionados'].initial = self.instance.toppings or []
    
    def save(self, commit=True):
        # Convertir selección de checkboxes a JSON
        instance = super().save(commit=False)
        instance.toppings = list(self.cleaned_data['toppings_seleccionados'])
        if commit:
            instance.save()
        return instance

@admin.register(PedidoCono)
class PedidoConoAdmin(admin.ModelAdmin):
    form = PedidoConoForm
    list_display = ['cliente', 'variante', 'tamanio_cono', 'fecha_pedido', 'get_toppings_display']
    list_filter = ['variante', 'tamanio_cono', 'fecha_pedido']
    search_fields = ['cliente']
    readonly_fields = ['fecha_pedido']
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('cliente',)
        }),
        ('Detalles del Pedido', {
            'fields': ('variante', 'tamanio_cono', 'toppings_seleccionados')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_pedido',),
            'classes': ('collapse',)
        }),
    )
    
    def get_toppings_display(self, obj):
        toppings = obj.toppings or []
        if not toppings:
            return "Sin toppings"
        return ", ".join(toppings)
    get_toppings_display.short_description = 'Toppings'
    
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
            self.message_user(request, f'Pedido para {obj.cliente} guardado exitosamente.')
        except Exception as e:
            self.message_user(request, f'Error al guardar: {str(e)}', level='ERROR')