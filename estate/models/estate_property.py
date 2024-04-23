from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property_estate'
    _description = 'Property of estate module XDc' 
    _rec_name = 'title'
    _order = 'sequence, id desc'

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange("garden")
    def _garden_on_change(self):
        if self.garden:
            self.garden_orientation = "North"
            self.garden_area = 10
        else:
            self.garden_orientation = "South"
            self.garden_area = None

    sequence = fields.Integer('Sequence', default=1, help="Used to order property. Lower is better.")
    title = fields.Char(string='Name of the property')
    description = fields.Char(string='Description', required=True)
    postcode = fields.Char(string='Postcode', required=True)
    date_availability = fields.Date(string='Available from', required=True, copy=False,
                                    default=lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    best_offer = fields.Float(string="Best offer", compute="_best_offer")
    bedroom = fields.Integer(string='Bedroom', default='3')
    facade = fields.Integer(string='Facade')
    garage = fields.Boolean(string='Garage')
    roof = fields.Boolean(string="Roof", default=True)
    garden = fields.Boolean(string='Garden')
    garden_orientation = fields.Selection(
        [
            ("North", "North"),
            ("South", "South"),
            ("West", "West"),
            ("East", "East"),
        ],
        string='Garden orientation',
        default='North',
        required=True
    )
    garden_area = fields.Float(string='Garden Area')
    living_area = fields.Float(string='Living Area')
    total_area = fields.Float(string='Total Area', compute="_compute_total")
    active = fields.Boolean(string='Active', default=True)
    status = fields.Selection(
        [
            ("New", "New"),
            ("Offer received", "Offer recieved"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Canceled", "Canceled"),
        ],
        string='Satus',
        required=True,
        default='New',
        copy=False
    )
    property_type_id = fields.Many2one(comodel_name="estate.property_estate_type", string="Property type")
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    tags_ids = fields.Many2many(comodel_name="estate.property_estate_tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property_estate_offer", inverse_name="property_id",
                                string="Offers")
    # model_id = fields.Many2one(comodel_name="estate.property_estate_type")

    _sql_constraints = [
        ('positive_price', 'CHECK(expected_price > 0)', 'The price must be strictly positive')
    ]

    def action_cancel(self):
        for record in self:
            record.status = "Canceled"
            return True

    def action_sold(self):
        for record in self:
            if record.status == "Canceled":
                raise UserError("Cancelled properties cannot be sold!")
            else:
                record.status = 'Sold'
            return True

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion(self):
        for record in self:
            if record.status not in ["New", "Canceled"]:
                raise UserError("Only New ans Cancelled properties can be deleted!")


