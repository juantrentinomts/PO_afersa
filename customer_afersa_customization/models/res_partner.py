from odoo import api, models, fields, exceptions
import logging
from odoo.exceptions import ValidationError
import re
_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = "res.partner"

    wtransnet = fields.Char(string="URL WTransnet", help="URL WTransnet")
    new_cif = fields.Char(
        string="CIF/NIF",
        related='vat',
        store=True,
    )
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', required=True)

    

    @api.onchange('new_cif', 'country_id')
    def _onchange_new_cif(self):
        if self.new_cif:
            if self.country_id.code == False:
                return {
                    'warning': {
                        'title': "Falta pais",
                        'message': "No hay pais seleccionado",
                    }
                }
            new_cif = "{0}{1}".format(self.country_id.code, self.new_cif.upper())
            # Validar si es un CIF o un DNI
            new_cif = new_cif.replace(self.country_id.code, "")
            _logger.error(new_cif) # Asegurarse de que sea mayúsculas para la validación
            if self._is_valid_cif(new_cif):
                # Es un CIF válido
                self.vat = "{0}{1}".format(self.country_id.code, new_cif)
            elif self._is_valid_dni(new_cif):
                # Es un DNI válido
                self.vat = "{0}{1}".format(self.country_id.code, new_cif)
            else:
                # Si no es válido, calcular la letra correcta y mostrar un mensaje
                if re.match(r'^\d{8}[A-Z]?$', new_cif):  # Verificar si parece un DNI
                    correct_letter = self._calculate_dni_letter(new_cif[:-1])
                    return {
                        'warning': {
                            'title': "DNI inválido",
                            'message': f"El DNI introducido no es válido. La letra correcta debería ser '{correct_letter}'.",
                        }
                    }
                elif re.match(r'^[A-HJ-NP-SUVW]\d{7}[0-9A-J]?$', new_cif):  # Verificar si parece un CIF
                    correct_control = self._calculate_cif_control(new_cif[:-1])
                    return {
                        'warning': {
                            'title': "CIF inválido",
                            'message': f"El CIF introducido no es válido. El control correcto debería ser '{correct_control}'.",
                        }
                    }
                else:
                    return {
                        'warning': {
                            'title': "Valor inválido",
                            'message': "El valor introducido no es un CIF ni un DNI válido.",
                        }
                    }

    def _is_valid_cif(self, cif):
        """
        Valida si el CIF es correcto.
        """
        cif_regex = r'^[A-HJ-NP-SUVW]\d{7}[0-9A-J]$'
        if not re.match(cif_regex, cif):
            return False
        return cif[-1] == self._calculate_cif_control(cif[:-1])

    def _is_valid_dni(self, dni):
        """
        Valida si el DNI es correcto.
        """
        dni_regex = r'^\d{8}[A-Z]$'
        if not re.match(dni_regex, dni):
            return False
        return dni[-1] == self._calculate_dni_letter(dni[:-1])

    def _calculate_cif_control(self, cif_body):
        """
        Calcula el control (número o letra) de un CIF.
        """
        digits = cif_body[1:]
        even_sum = sum(int(d) for i, d in enumerate(digits) if i % 2 == 1)
        odd_sum = sum(sum(divmod(int(d) * 2, 10)) for i, d in enumerate(digits) if i % 2 == 0)
        total = even_sum + odd_sum
        calculated_control = str((10 - (total % 10)) % 10)

        if cif_body[0] in "KLMNPQRSW":  # Letras que requieren control como letra
            return "JABCDEFGHI"[int(calculated_control)]
        else:
            return calculated_control

    def _calculate_dni_letter(self, dni_body):
        """
        Calcula la letra de un DNI.
        """
        valid_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        return valid_letters[int(dni_body) % 23]
