from odoo import api, models, fields, exceptions
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    initial_direction = fields.Char(string="Dirección de inicio")
    end_direction = fields.Char(string="Dirección de llegada")
    distance = fields.Float(string="Distance (km)")
    partner_id = fields.Many2one('res.partner', string='Vendor',required=False, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    afersa_order_id = fields.Many2one("sale.order", string="Afersa Id Venta")
    additional_addresses_ids = fields.One2many(
        comodel_name="additional.addresses",
        inverse_name='purchase_order_id',
        string="Direcciones adicionales"
    )
    afersa_cancelation_id = fields.Many2one("sale.cancelations")


    def button_cancel_new(self):
        return {
            'name': 'Cancelar compra',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.afersa.cancelations',
            'view_type': 'form',
            'target': 'new',
            # Otros parámetros opcionales, como 'context' o 'domain'
        }    

    def action_view_cancelation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Motivo de cancelación',
            'view_mode': 'form',
            'res_model': 'sale.cancelations',
            'domain': [('afersa_cancelation_id', '=', self.id)],
            'res_id': self.afersa_cancelation_id.id,
            'context': {'default_afersa_cancelation_id': self.id},
        }    

    
