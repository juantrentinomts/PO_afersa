from odoo import api, models, fields, exceptions
import logging

_logger = logging.getLogger(__name__)

class AdditionalDirections(models.Model):
    _name = "additional.addresses"
    _description = "Direcciones adicionales"    

    sale_order_id = fields.Many2one('sale.order',string="Order Reference")    
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Reference')
    
    addresses_type = fields.Selection([('delivery', 'Entrega'), ('collection', 'Recogida')], required=True, string="Tipo de dirección")
    addresses = fields.Char(string="Dirección")

    @api.model
    def create(self, values):
        # Crear la dirección adicional
        address = super(AdditionalDirections, self).create(values)

        if not address.sale_order_id:
            sale = self.env['sale.order'].search([("name", "=", address.purchase_order_id.origin)])
            address.update({
                "sale_order_id": sale.id
            })

        # Sincronizar con sale.order si sale_order_id está presente
        if address.sale_order_id.afersa_purchase_id:
            address.update({
                "purchase_order_id": address.sale_order_id.afersa_purchase_id
            })

        return address
