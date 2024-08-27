# product_services.py
from django.db.models import Max
from pay.models import Productos

def assign_order(producto):
    if not producto.pk:  # Si el producto es nuevo
        max_order = Productos.objects.aggregate(Max('order'))['order__max']
        if max_order is None:
            producto.order = 1
        else:
            producto.order = max_order + 1
    else:  # Si se está actualizando un producto existente
        original = Productos.objects.get(pk=producto.pk)
        if original.order != producto.order:  # Solo reordenar si el orden cambia
            # Obtener todos los productos excepto el actual
            productos = Productos.objects.exclude(pk=producto.pk).order_by('order')
            # Reasignar los números de orden a todos los productos
            new_order_list = []
            current_order = 1
            for p in productos:
                if current_order == producto.order:
                    current_order += 1
                new_order_list.append((p.pk, current_order))
                current_order += 1

            # Guardar los cambios en orden
            for pk, new_order in new_order_list:
                Productos.objects.filter(pk=pk).update(order=new_order)
