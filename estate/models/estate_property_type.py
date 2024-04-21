from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property_estate_type'
    _description = 'Type property of estate module'
    _order = 'name'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(comodel_name="estate.property_estate", inverse_name="property_type_id")
    offer_ids = fields.One2many(comodel_name="estate.property_estate_offer", inverse_name="property_type_id")
    offer_count = fields.Integer(string="Offers", compute="_compute_offer_count")

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type must be unique')
    ]

    def estate_model_offer_action(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "estate.property_estate_offer",
            "domain": [('id', 'in', self.offer_ids.ids)],
            "name": "Offer view",
            'view_mode': 'tree',
        }

# class EstateOfferLine(models.Model):
#     _name = 'estate.property_estate_offer_line'
#     _description = 'Offer line for estate module'
#
#     model_id = fields.Many2one(comodel_name="estate.property_estate_type")
#
#     title = fields.Char(string="Title")
#     expected_price = fields.Char(string="Expected Price")
#     status = fields.Char(string="Status")
