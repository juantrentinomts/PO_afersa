from odoo import api, models, fields, exceptions


class Vehicles(models.Model):
    _name = "res.vehicle"
    _description = "Vehiculos"

    name = fields.Char(string="Matricula", required=True)
    vehicle_type = fields.Many2one('res.vehicle.type', string="Tipo de Vehiculo")
    vehicle_categories = fields.Many2many("res.vehicle.category", string="Categorias")
    contact_ids = fields.Many2many(
        'res.partner', 
        string='Owners',
        relation='vehicle_contact_rel',
        column1='vehicle_id',
        column2='contact_id'
    )

class VehiclesType(models.Model):
    _name = "res.vehicle.type"
    _description = "Tipo de Vehiculo"

    name = fields.Char(string="Modelo", required=True)


class VehiclesCategory(models.Model):
    _name = "res.vehicle.category"
    _description = "Categoria de Vehiculo"

    name = fields.Char(string="Categoria", required=True)
    color = fields.Integer("Color", required=True)

