from odoo import _, fields, models, exceptions
import base64
import logging
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)

class CancealtionsModal(models.TransientModel):
    _name = "sale.afersa.cancelations"

    negative_score = fields.Boolean(string="Generar puntuacion negativa", default=False)
    cancelation_type = fields.Many2one("sale.cancelation.type", string="Tipo de cancelación", required=True)

    def cancel_afersa(self):
        obj_to_cancel = self.env.context.get("active_model")
        if obj_to_cancel != 'sale.order' and obj_to_cancel != 'purchase.order':
            raise exceptions.UserError("Error")

        cancelation_new = self.env['sale.cancelations'].create({
            "negative_score": self.negative_score,
            "cancelation_type": self.cancelation_type.id
        })

        sale=self.env[obj_to_cancel].browse(self.env.context.get('active_id'))
        sale.update({
            "afersa_cancelation_id": cancelation_new.id
        })

        if self.negative_score:
            partner = self.env['res.partner'].browse(sale.partner_id.id)
            if partner.partner_score != '0':
                partner.update({
                    "partner_score": str(int(partner.partner_score) - 1)
                })

        if obj_to_cancel != 'sale.order':
           return sale.button_cancel()
        else:
           return sale.action_cancel()

class Cancelations(models.Model):
    _name = "sale.cancelations"

    negative_score = fields.Boolean(string="Generar puntuacion negativa", default=False)
    cancelation_type = fields.Many2one("sale.cancelation.type", string="Tipo de cancelación", required=True)

