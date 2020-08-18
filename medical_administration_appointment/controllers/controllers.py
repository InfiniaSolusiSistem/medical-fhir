# -*- coding: utf-8 -*-
from odoo import http

# class MedicalAppointment(http.Controller):
#     @http.route('/medical_appointment/medical_appointment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/medical_appointment/medical_appointment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('medical_appointment.listing', {
#             'root': '/medical_appointment/medical_appointment',
#             'objects': http.request.env['medical_appointment.medical_appointment'].search([]),
#         })

#     @http.route('/medical_appointment/medical_appointment/objects/<model("medical_appointment.medical_appointment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('medical_appointment.object', {
#             'object': obj
#         })