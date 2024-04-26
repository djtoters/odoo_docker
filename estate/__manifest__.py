# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Estanhjte",
    "version": "1.0",
    "category": "Sales/estate",
    "sequence": 1000,
    "summary": "Real estate module",
    "description": "",
    "website": "https://www.odoo.com/documentation/15.0/fr/developer/tutorials/getting_started/03_newapp.html",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        # 'views/estate_property_offer_view.xml',
        "views/estate_property_menu_view.xml",
        "views/template.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
