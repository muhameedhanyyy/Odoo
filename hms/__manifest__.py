{
    'name': 'HMS',
    'version': '1.0',
    'summary': '',
    'description': '',
    'author': '',
    'license': 'LGPL-3',
    'depends': ['base', 'crm'],
    'data': [
        # Security – groups must be loaded first, then access rules, then record rules
        'security/hms_groups.xml',
        'security/ir.model.access.csv',
        'security/hms_record_rules.xml',

        # Views
        'views/department_views.xml',
        'views/doctors_views.xml',
        'views/patient_views.xml',
        'views/patient_log_views.xml',
        'views/res_partner_views.xml',

        # Reports
        'report/patient_report_template.xml',
    ],
    'installable': True,
    'application': True,
}
