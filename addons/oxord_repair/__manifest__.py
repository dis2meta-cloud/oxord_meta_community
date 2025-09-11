# oxord_repair/__manifest__.py
{
    'name': 'Oxord Repair Customizations',
    'summary': 'Custom fields & workflows for Oxord Computer Solutions (Repairs & QC)',
    'version': '18.0.1.0.0',
    'category': 'Repair',
    'author': 'Oxord / Your Dev',
    'depends': ['repair', 'stock', 'sale_management', 'product', 'mail'],
    'data': [
        'security/oxord_groups.xml',
        'security/ir.model.access.csv',
        'views/repair_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
