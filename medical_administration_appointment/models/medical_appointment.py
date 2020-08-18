# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MedicalAppointment(models.Model):
    # FHIR Entity: Appointment (http://hl7.org/fhir/appointment.html)
    _name = "medical.appointment"
    _description = "Medical Appointment"
    _inherit = ["medical.abstract", "mail.thread", "mail.activity.mixin"]
    _order = "create_date DESC"

    name = fields.Char(string='Name')
    internal_identifier = fields.Char(string="Appointment")
    state = fields.Selection(
        string='Appointment Status', 
        selection=[
            ('proposed', 'Proposed'), 
            ('pending', 'Pending'),
            ('booked', 'Booked'),
            ('arrived', 'Arrived'),
            ('fulfilled', 'Fulfilled'),
            ('cancelled', 'Cancelled'),
            ('noshow', 'No-Show'),
            ('entered-in-error', 'Entered in Error'),
            ('checked-in', 'Checked In'),
            ('waitlist', 'Waitlist'),
        ]
    )  # FHIR Field: status
    cancellation_reason_id = fields.Many2one(comodel_name='medical.appointment.cancellation.reason', string='Cancellation Reason')
    create_date = fields.Datetime(string='Create Date')    
    # FHIR Field: cancellationReason    

class MedicalAppointmentCancellationReason(models.Model):
    # FHIR Entity: Cancellation Reason (http://hl7.org/fhir/codesystem-appointment-cancellation-reason.html)
    _name = 'medical.appointment.cancellation.reason'
    _description = 'Medical Cancellation Appointment Reason'
    _inherit = ["medical.abstract"]
    _order = "code DESC"

    name = fields.Char(string='Display Name', required=True)
    code = fields.Char(string='Code', required=True)
    parent_id = fields.Many2one(comodel_name='medical.appointment.cancellation.reason', string='Parent')
    level = fields.Integer(string='Level')
    
    
    
