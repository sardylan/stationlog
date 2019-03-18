from odoo import models, fields


class Armi(models.Model):
    _name = "awards_naval.armi"

    callsign = fields.Char(
        string="Callsign",
        required=True
    )

    reference = fields.Char(
        string="Reference",
        required=True
    )
