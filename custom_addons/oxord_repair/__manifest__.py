{
    'name': 'OXORD Repair',
    'version': '1.0',
    'summary': 'Custom Repair Workflow for OXORD',
    'description': 'Customized repair order workflow and fields for OXORD process',
    'author': 'OXORD Computer Solutions',
    'depends': ['repair', 'base', 'stock'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/repair_order_view.xml',
        'views/repair_action.xml',  
        'views/repair_menu.xml',
        'data/company_data.xml',
        'data/repair_sequence.xml',
    ],
    'installable': True,
    'application': True,
}
