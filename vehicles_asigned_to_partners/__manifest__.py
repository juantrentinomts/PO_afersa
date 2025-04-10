{
    'name': "Assign Vehicles to Partner",
    'version': '1.0',
    'summary': "vehicles_asigned_to_partners",
    'description': "Assign Vehicles to Partner by MTS",
    'author': 'MTS',
    'company': 'MTS',
    'maintainer': 'MTS',
    'website': "https://www.madetosoft.com",
    'depends': ["contacts"],
    'data': [
        "views/res_vehicle_views.xml",
        "views/res_vehicle_category.xml",
        'security/ir.model.access.csv',
        "views/res_vehicle_type_views.xml"
    ],
    'license': "",
    'installable': True,
    'application': True,
}
