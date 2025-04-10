from odoo import api, models, fields, exceptions
import logging

_logger = logging.getLogger(__name__)

class Product(models.Model):
    _inherit = "product.template"

    addr_code = fields.Char(string="Codigo de dirección")
