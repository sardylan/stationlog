from odoo import models, fields

SELECTION_TECHNOLOGY = [
    ("analogradio", "Analogic radio link"),
    ("echolink", "Echolink"),
    ("fusion", "Room in System Fusion"),
    ("tg", "DMR Talk Group")
]


class Conference(models.Model):
    _name = "repeaters.conference"
    _inherit = "mail.thread"
    _description = "Conference"

    name = fields.Char(
        string="Name",
        help="Name",
        required=True,
        track_visibility="onchange"
    )

    technology = fields.Selection(
        string="Technology",
        help="Technology",
        selection=SELECTION_TECHNOLOGY,
        required=True,
        track_visibility="onchange"
    )

    appliance_ids = fields.One2many(
        string="Appliances",
        help="Appliances",
        comodel_name="repeaters.appliance",
        inverse_name="conference_id",
        readonly=True,
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note",
        help="Note",
        track_visibility="onchange"
    )
