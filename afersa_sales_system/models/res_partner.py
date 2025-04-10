from odoo import api, models, fields, exceptions


class Partner(models.Model):
    _inherit = "res.partner"

    partner_score = fields.Selection(
        [
            ('0', '0 Star'),
            ('1', '1 Star'),
            ('2', '2 Stars'),
            ('3', '3 Stars'),
            ('4', '4 Stars'),
            ('5', '5 Stars'),
        ],
        string='Puntuación contacto',
        default='5',
    )
