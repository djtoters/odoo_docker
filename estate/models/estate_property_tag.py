from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property_estate_tag'
    _description = 'Tag property of estate module'
    _order = 'name'

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The property tag must be unique')
    ]
