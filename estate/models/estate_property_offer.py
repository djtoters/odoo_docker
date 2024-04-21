import pdb
from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstateOffer(models.Model):
    _name = 'estate.property_estate_offer'
    _description = 'Offer for estate module'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection(
        [
            ('Accepted', 'Accepted'),
            ('Refused', 'Refused'),
        ],
        string='Status',
        copy=False
    )
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property_estate', string='Property', required=True)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Date deadline', compute="_date_deadline", inverse="_inverse_validity")
    property_type_id = fields.Many2one(related="property_id.property_type_id", stored=True)

    _sql_constraints = [
        ('positive_price_offer', 'CHECK(price > 0)', 'The offer must be strictly positive')
    ]

    @api.depends("validity")
    def _date_deadline(self):
        create_date = fields.Date.today()
        for record in self:
            record.date_deadline = create_date + timedelta(days=record.validity)

    @api.depends("date_deadline")
    def _inverse_validity(self):
        create_date = fields.Date.today()
        for record in self:
            delta = record.date_deadline - create_date
            record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.status != "Offer Accepted":
                record.status = "Accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.status = "Offer Accepted"
            else:
                raise UserError("Too late! \n An offer has already been accepted!")

    def action_refuse(self):
        for record in self:
            record.status = "Refused"

    @api.constrains("price")
    def _check_price_offer(self):
        for record in self:
            limit_offer = record.property_id.expected_price * 0.9
            if record.price < limit_offer:
                raise ValidationError("The selling price must be at least 90% of the expected price!")

    @api.model
    def create(self, vals):
        # Créez d'abord l'offre normalement
        record = super().create(vals)

        # Vérifiez si l'offre est supérieure à toutes les autres pour la propriété spécifique
        # property = self.env['estate.property_estate'].browse(vals['property_id'])
        # if property.offer_ids and record.price <= max(property.offer_ids.mapped('price')):
        #     raise UserError("The new offer should be higher than all existing offers.")
        print("Blabla")
        # Modifiez l'état de la propriété

        record.property_id.status = 'Offer received'

        # property_obj = self.env['estate.property_estate'].browse(record.property_id)
        # property_obj.write({'status': 'Offer received'})

        return record




# class MyClass(models.Model):
#     _name = 'my.class'
#
#     name = fields.Char(string='Name')
#     other_class_id = fields.Many2one('other.class', string='Other Class')
#
#     def update_other_class_field(self):
#         other_class = self.env['other.class'].browse(self.other_class_id.id)
#         other_class.write({'field_to_update': 'New Value'})
