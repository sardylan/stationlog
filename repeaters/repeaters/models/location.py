from odoo import models, fields

SELECTION_ICON_TYPE = [
    ("generic", "Generic"),
    ("analog", "Analog FM"),
    ("dstar", "D-Star"),
    ("dmr", "DMR"),
    ("c4fm", "C4FM"),
    ("aprs12", "APRS 1.2 kb/s"),
    ("aprs96", "APRS 9.6 kb/s")
]


class Location(models.Model):
    _name = "repeaters.location"
    _inherit = "mail.thread"
    _description = "Location"

    name = fields.Char(
        string="Name",
        help="Location name",
        required=True,
        track_visibility="onchange"
    )

    display = fields.Boolean(
        string="Display",
        help="Display in frontend",
        require=True,
        default=True,
        track_visibility="onchange"
    )

    icon_type = fields.Selection(
        string="Icon type",
        help="Icon type",
        selection=SELECTION_ICON_TYPE,
        required=True,
        default="generic",
        track_visibility="onchange"
    )

    latitude = fields.Float(
        string="Latitude",
        help="Latitude",
        digits=(9, 6),
        track_visibility="onchange"
    )

    longitude = fields.Float(
        string="Longitude",
        help="Longitude",
        digits=(9, 6),
        track_visibility="onchange"
    )

    altitude = fields.Integer(
        string="Altitude",
        help="Altitude",
        track_visibility="onchange"
    )

    station_ids = fields.One2many(
        string="Stations",
        help="Installed stations",
        comodel_name="repeaters.station",
        inverse_name="location_id",
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note",
        help="Note",
        track_visibility="onchange"
    )
