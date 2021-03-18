import pandas as pd


def generate_sales_report(invoices):
    columns = [
        'Marketplace', 'Invoice Id', 'Transaction Id', 'Transaction Time', 'Transaction Type', 'Adjustment',
               'ASIN', 'Vendor SKU', 'Title', 'Item Name', 'Item Type', 'In-App Subscription Term',
               'In-App Subscription Status', 'Units', 'Usage Time', 'Marketplace Currency', 'Sales Price',
               'Estimated Earnings', 'App User ID', 'Receipt ID', 'Digital Order ID'
    ]
    items_rows = []
    for invoice in invoices:
        for item in invoice.receipt.transaction.items.all():
            trial = ''
            if item.item.category == 1:
                if item.trial:
                    trial = 'Trial'
                else:
                    trial = 'Paid'
            item_dict = {
                'Marketplace': invoice.receipt.transaction.marketplace.name,
                'Invoice Id': invoice.invoice_id,
                'Transaction Id': invoice.receipt.transaction.id,
                'Transaction Time': invoice.receipt.transaction.time,
                'Transaction Type': 'Refund' if invoice.receipt.transaction.refund else 'Charge',
                'Adjustment': 'Yes' if invoice.receipt.transaction.adjustment else 'No',
                'ASIN': item.item.ASIN,
                'Vendor SKU': invoice.receipt.transaction.vendor.SKU,
                'Title': item.item.title,
                'Item Name': item.item.name,
                'Item Type': item.item.category,
                'In-App Subscription Term': item.item.subscription_term if item.item.category == 1 else '',
                'In-App Subscription Status': trial,
                'Units': item.units,
                'Usage Time': item.units * 60 if isinstance(item.item.category, int) and 0 < item.item.category <= 5 else 0,
                'Marketplace Currency': invoice.receipt.transaction.marketplace.currency,
                'Sales Price': item.total_value,
                'Estimated Earnings': item.total_earnings,
                'App User ID': invoice.receipt.transaction.customer.app_id,
                'Receipt ID': invoice.receipt.receipt_id,
                'Digital Order ID': invoice.receipt.transaction.transaction_id
            }
            items_rows.append(item_dict)
    df = pd.DataFrame(items_rows, columns=columns)
    return df
