from odoo import http

class NewPage(http.Controller):
    @http.route('/new-page/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('estate.index')
