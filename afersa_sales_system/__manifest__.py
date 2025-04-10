{
    'name': "Afersa Custom Sales System",
    'version': '1.0',
    'summary': "afersa_sales_system",
    'description': "Afersa Custom Sales System by MTS",
    'author': 'MTS',
    'company': 'MTS',
    'maintainer': 'MTS',
    'website': "https://wwpurchasew.madetosoft.com",
    'depends': ["sale_management", "purchase", 'project','sale_project', 'stock', 'vehicles_asigned_to_partners'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_inheit.xml",
        "views/sale_view_inherit.xml",
        "views/purchase_view_inherit.xml",
        "views/task_view_inherit.xml",
        "views/res_partner_inherit.xml",
        "views/sale_cancelation_type_views.xml",
        "wizards/cancelation_modal_views.xml"
        
    ],
    'license': "",
    'installable': True,
    'application': True,
}
