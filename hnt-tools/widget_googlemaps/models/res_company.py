from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.company"

    widget_googlemaps_api_key = fields.Char(
        string="Google Maps API Key",
        help="Google Maps API key for JS Api",
        default=""
    )
