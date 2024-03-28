{
    'name': 'Real Estate Complaints',
    'version': '1.0',
    'summary': 'Module for managing real estate complaints',
    'sequence': -100,
    'description': """Real Estate Complaints Management""",
    'category': 'Productivity',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail','website'],
    'data': [
        'data/sequence.xml',
        'data/email_template.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/complaint_view.xml',
        'views/complaint_template.xml',
    ],    'qweb': [
        'reports/complaint_report_template.xml',  
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

