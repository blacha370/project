from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'address', views.AddressViewSet)
router.register(r'company', views.CompanyViewSet)
router.register(r'customer', views.CustomerViewSet)
router.register(r'marketplace', views.MarketplaceViewSet)
router.register(r'tax', views.TaxViewSet)
router.register(r'item', views.ItemViewSet)
router.register(r'sold_item', views.SoldItemViewSet)
router.register(r'transaction', views.TransactionViewSet)
router.register(r'receipt', views.ReceiptViewSet)
router.register(r'invoice', views.InvoiceViewSet)
router.register(r'advance_invoice', views.AdvanceInvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add_customer', views.AddCustomer.as_view()),
    path('create_tax', views.CreateTax.as_view()),
    path('create_item', views.CreateItem.as_view()),
    path('create_transaction', views.CreateTransaction.as_view()),
    path('create_receipt', views.CreateReceipt.as_view()),
    path('create_invoice', views.CreateInvoice.as_view()),
    path('create_advance_invoice', views.CreateAdvanceInvoice.as_view()),
    path('end_invoice', views.EndInvoice.as_view()),
    path('generate_sales_report/<int:year>/<int:month>', views.GenerateSalesReport.as_view())
]
