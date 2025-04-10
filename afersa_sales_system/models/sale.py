from odoo import api, models, fields, exceptions
import logging
import requests
import re
import webbrowser

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    initial_direction = fields.Char(string="Dirección de inicio")
    end_direction = fields.Char(string="Dirección de llegada")
    afersa_purchase_id = fields.Many2one("purchase.order", string="Afersa Id Compra")
    afersa_cancelation_id = fields.Many2one("sale.cancelations")
    distance = fields.Float(string="Distance (km)")

    additional_addresses_ids = fields.One2many(
        comodel_name="additional.addresses",
        inverse_name='sale_order_id',
        string="Direcciones adicionales"
    )

    def compute_distance(self):
        pattern = r'\b\d{5}\b'
        for order in self:
            if order.initial_direction and order.end_direction:
                google_maps_api_key = self.env['ir.config_parameter'].get_param('api_google_key')
                url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={order.initial_direction}&destinations={order.end_direction}&key={google_maps_api_key}"
                response = requests.get(url)
                order.distance = 0.0
                start_zip = ''
                end_zip = ''
                if response.status_code == 200:
                    result = response.json()
                    if result['rows']:
                        elements = result['rows'][0]['elements'][0]
                        if elements['status'] == 'OK':
                            distance = elements['distance']['value'] / 1000  # distance in km
                            start_zip_group = re.search(pattern, result['origin_addresses'][0])
                            end_zip_group = re.search(pattern, result['destination_addresses'][0])
                            if start_zip_group and end_zip_group:
                                start_zip = start_zip_group.group(0)
                                end_zip = end_zip_group.group(0)
                            else:
                                raise exceptions.UserError("No se pudo obtener el código postal de una de las direcciones. Verifica que las direcciones sean válidas.")

                if start_zip and end_zip:
                    lines = []
                    product = self.env['product.product'].search([
                        ('addr_code', '=', f'{start_zip[0:2:1]}-{end_zip[0:2:1]}')
                    ], limit=1)


                    if product:
                        lines.append((0, 0, {
                            "product_id" : product.product_variant_id.id,
                            "product_template_id": product.id,
                            "name": product.name
                        }))
                        order.order_line = lines
                        order.distance = distance
                    else:
                        return {
                            'type' : 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'message': f'No se ha encontrado el producto con la referencia {start_zip[0:2:1]}-{end_zip[0:2:1]}',
                                'sticky': True
                            }
                        }

                return {
                    'type': 'ir.actions.act_url',
                    'url': f"https://www.google.com/maps/dir/?api=1&origin={order.initial_direction}&destination={order.end_direction}",
                    'target': '_blank'
                }   
                     
            else:
                return {
                    'type' : 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'Se tienen que indicar las dos direcciones para calcular la distancia del reccorido',
                        'sticky': True
                    }
                }

    def create_purchase(self):
        purchase_order_lines = []

        # Fomateamos las lines de la venta pra copiarlas en la compra nueva
        for line in self.order_line:
            purchase_order_lines.append([0,0,{
                "product_id": line.product_id.id,
                "product_qty": float(line.product_uom_qty),
                "price_unit": line.price_unit,
                "taxes_id": line.tax_id
            }])

        #    
        new_purchase = self.env['purchase.order'].create({
            'user_id': self.user_id.id,
            'order_line': purchase_order_lines,
            "origin": self.name,
            "afersa_order_id": self.id,
            "initial_direction": self.initial_direction,            
            "end_direction": self.end_direction,
            "distance": self.distance
        })
        for line in self.additional_addresses_ids:
            line.update({
                "purchase_order_id": new_purchase.id
            })
            _logger.error(line.purchase_order_id)
        self.update({
            "afersa_purchase_id": new_purchase.id
        })

    def action_view_purchase_afersa(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Compras Afersa',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'domain': [('afersa_order_id', '=', self.id)],
            'res_id': self.afersa_purchase_id.id,
            'context': {'default_afersa_order_id': self.id},
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

    def action_cancel_new(self):
        
         # super().action_cancel()
        return {
            'name': 'Cancelar pedido',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.afersa.cancelations',
            'view_type': 'form',
            'target': 'new',
            # Otros parámetros opcionales, como 'context' o 'domain'
        }

class CancelationsType(models.Model):
    _name = "sale.cancelation.type"
    _description = "Tipo de Cancelación"

    name = fields.Char(string="Motivo", required=True)