from odoo import models, fields


class Armi(models.Model):
    _name = "awards_naval.armi"
    _rec_name = "reference"

    reference = fields.Char(
        string="Reference",
        required=True
    )

    callsign = fields.Char(
        string="Callsign",
        required=True
    )

    name = fields.Char(
        string="Name"
    )

    qualifica = fields.Char(
        string="Qualifica"
    )

    marina = fields.Char(
        string="Marina"
    )

    svc = fields.Boolean(
        string="SVC",
        default=False
    )
