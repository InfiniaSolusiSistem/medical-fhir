# -*- coding: utf-8 -*-

{
    "name": "Medical Administration: Appointment",
    "summary": "Medical administration: Appointment module",
    "version": "12.0.1.0.0",
    "author": "Infinia Solusi Sistem",
    "website": "https://infinia.id",
    "category": "Medical",
    "license": "LGPL-3",
    "depends": ["medical_base"],
    "data": [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/medical_appointment_view.xml',
        'views/templates.xml',
    ],
    "demo": [],
    "application": False,
    "installable": True,
    "auto_install": True,
}
