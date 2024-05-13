from django.urls import path, include
from rest_framework import routers

from pay.views import SolicitudViewSet, ConsultaViewSet, ConsultaExtendViewSet, webhook
from pay.views.discountViews import DiscountView, GetUserByDiscountView, UserDiscountsView, GetDiscountByVerificationCodeView
from pay.views.productsView import ProductosListCreateView, ProductosRetrieveUpdateDeleteView
from pay.views.allTransactionsView import AllTransactionsView

router = routers.DefaultRouter() 
router.register(r'discount', DiscountView, 'discount')

discount_router = routers.DefaultRouter()
discount_router.register(r'discount', DiscountView, 'discount')

urlpatterns = [

    path('solicitud', SolicitudViewSet.as_view(), name="solicitud_pago"), 

    path('consulta_transaccion', ConsultaViewSet.as_view(), name="consulta_transaccion"), 
    path('consulta_extend/<int:pk>', ConsultaExtendViewSet.as_view(), name="consulta_transaccion"),

    
    path('webhook', webhook.as_view(), name="consulta_transaccion"),

    # Incluir las URLs generadas por ambos routers
    path("discounts/", include(discount_router.urls)),

    path("discount/user/<int:discount_id>/", GetUserByDiscountView.as_view(), name='get_user_by_discount'),

    path("discounts/user/", UserDiscountsView.as_view(), name="get_user_disocunts"),

    path('discount/verification_code/<str:verification_code>/', GetDiscountByVerificationCodeView.as_view(), name='get_discount_by_verification_code'),

    path('productos/', ProductosListCreateView.as_view(), name='productos-list-create'),
    path('productos/<int:pk>/', ProductosRetrieveUpdateDeleteView.as_view(), name='productos-retrieve-update-delete'),
    
    path('transactions/', AllTransactionsView.as_view(), name='all_transactions'),
]

# TODO: a consulta extend agregarle el datelle de la compra 
# TODO: que solo retorne datos ya pagados (con status 2)