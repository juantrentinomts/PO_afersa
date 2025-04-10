from odoo import api, models, fields, exceptions


class Partner(models.Model):
    _inherit = "res.partner"

    vehicles_ids = fields.Many2many(
        'res.vehicle', 
        string='Vehicles',
        relation='vehicle_contact_rel',
        column1='contact_id',
        column2='vehicle_id'
    )
