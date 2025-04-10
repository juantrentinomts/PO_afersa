{
    'name': 'Multi-Company Product Sharing',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Allows a single product to be shared across multiple companies',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        "views/product_views.xml"
    ],
    'installable': True,
    'application': False,
}
