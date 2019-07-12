from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    widget_googlemaps_api_key = fields.Char(
        string="Google Maps API Key",
        help="Google Maps API key for JS Api",
        default=""
    )

    def __init__(self, pool, cr):
        super().__init__(pool, cr)

        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(["widget_googlemaps_api_key"])

        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(["widget_googlemaps_api_key"])
