from odoo import models, fields, api


class Station(models.Model):
    _name = "repeaters.station"
    _inherit = "mail.thread"
    _description = "Station"
    _rec_name = "callsign"
    _order = "callsign ASC"

    _sql_constraints = [
        ("callsign_uniq", "UNIQUE(callsign)", "Callsign already present")
    ]

    callsign = fields.Char(
        string="Callsign",
        required=True,
        translate=False,
        track_visibility="onchange"
    )

    location_id = fields.Many2one(
        string="Location",
        help="Location",
        comodel_name="repeaters.location",
        track_visibility="onchange"
    )

    appliance_ids = fields.One2many(
        string="Appliances",
        help="Appliances",
        comodel_name="repeaters.appliance",
        inverse_name="station_id",
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note",
        track_visibility="onchange"
    )

    @api.model
    def create(self, vals):
        if "callsign" in vals and vals["callsign"]:
            vals["callsign"] = vals["callsign"].strip().upper()

        return super().create(vals)

    @api.multi
    def write(self, vals):
        if "callsign" in vals and vals["callsign"]:
            vals["callsign"] = vals["callsign"].strip().upper()

        return super().write(vals)

    @api.onchange("callsign")
    def onchange_callsign(self):
        for rec in self:
            if rec.callsign:
                rec.callsign = rec.callsign.strip().upper()
