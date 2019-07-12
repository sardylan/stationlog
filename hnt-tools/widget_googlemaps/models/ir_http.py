from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def webclient_rendering_context(self):
        res = super().webclient_rendering_context()

        if self.env.user.widget_googlemaps_api_key:
            api_key = self.env.user.widget_googlemaps_api_key
        elif self.env.user.company_id.widget_googlemaps_api_key:
            api_key = self.env.user.company_id.widget_googlemaps_api_key
        else:
            parameter_obj = self.env["ir.config_parameter"].sudo()
            api_key = parameter_obj.get_param("widget_googlemaps.api_key", default="")

        res["widget_googlemaps_api_key"] = api_key or ""

        return res
