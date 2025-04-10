from odoo import api, models, fields, exceptions
import logging

_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = "project.task"

    company_currency_id = fields.Many2one(
        string='Company Currency',
        related='company_id.currency_id', readonly=True,
    )

    sale_order_price = fields.Monetary(string='Base imponible venta', related='sale_order_id.amount_untaxed', currency_field='company_currency_id',store=True, readOnly=False)
    purchase_order_price = fields.Monetary(string='Base imponible compra', related='sale_order_id.afersa_purchase_id.amount_untaxed',currency_field='company_currency_id', store=True,readOnly=False)
    provider_id = fields.Many2one("res.partner", string="Proveedor", related="sale_order_id.afersa_purchase_id.partner_id", store=True)
    initial_direction = fields.Char(string="Origen",  related='sale_order_id.initial_direction')
    end_direction = fields.Char(string="Destino",  related='sale_order_id.end_direction')
    charge_date = fields.Date("Fecha de carga")
    vehicle_id = fields.Many2one(
        'res.vehicle', 
        string='Vehiculo',
        domain="[('contact_ids', 'in', provider_id)]"
    )
    customer_reference = fields.Char(string="Referencia cliente")

    
    def action_view_purchase_afersa(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pedido de Compra',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'domain': [('afersa_order_id', '=', self.sale_order_id)],
            'context': {'default_afersa_order_id': self.sale_order_id},
            'res_id': self.sale_order_id.afersa_purchase_id.id,
        }
    
    @api.onchange("sale_order_price")
    def recalculate_sale_order_price(self):
    	self.sale_order_id.order_line[0].write({
    	     "price_unit": self.sale_order_price
    	})
    	
    @api.onchange("purchase_order_price")
    def recalculate_sale_order_price(self):
    	self.sale_order_id.afersa_purchase_id.order_line[0].write({
    	     "price_unit": self.purchase_order_price
    	})
   
