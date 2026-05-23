{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_views.xml',
        'views/doctors_views.xml',
        'views/patient_views.xml',
	'views/patient_log_views.xml',

    ],
    'installable': True,
    'application': True,
}
