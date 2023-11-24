from rest_framework import viewsets
from pay.serializer import SavedDiscountsSerializer
from pay.models.transaction import SavedDiscounts
class SavedDiscountsView(viewsets.ModelViewSet):
    serializer_class=SavedDiscountsSerializer
    queryset=SavedDiscounts.objects.all()