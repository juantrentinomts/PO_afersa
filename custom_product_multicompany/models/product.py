from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Cambiamos la relación de la compañía para permitir multi-compañía
    company_ids = fields.Many2many(
        'res.company',
        string='Companies',
        help='The companies that can use this product.'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        index=True,
        help="Company that this product belongs to.",
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        """
        Redefine el método search para aplicar el dominio en función de `company_ids` del usuario.
        """
        _logger.error(self.env.user.has_group('base.group_multi_company'))
        if self.env.user.has_group('base.group_multi_company'):
            # Obtener las compañías a las que el usuario tiene acceso
            user_companies = self.env.context.get("allowed_company_ids")
            if user_companies:
                # Ajustar el dominio para productos visibles en cualquiera de las compañías del usuario
                company_domain = [('company_ids', 'in', user_companies)]

                if len(args) != 0:
                    args = ['&'] + company_domain + args
                else:
                    args = company_domain


                _logger.error(args)
        return super(ProductTemplate, self).search(args, offset=offset, limit=limit, order=order)

    _sql_constraints = [
        ('unique_product_per_company',
         'UNIQUE(name, default_code, company_ids)',
         'The product must be unique within the selected companies.')
    ]
