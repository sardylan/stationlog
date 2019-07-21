import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


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

    location_icon_id = fields.Many2one(
        string="Icon",
        help="Icon",
        comodel_name="repeaters.location_icon",
        required=True,
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

    position = fields.Char(
        string="Position",
        help="Location position"
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


class LocationIcon(models.Model):
    _name = "repeaters.location_icon"
    _description = "Location icon"

    _sql_constraints = [
        ("name_uniq", "UNIQUE(name)", "Icon name already exists")
    ]

    name = fields.Char(
        string="Name",
        help="Name of the icon",
        required=True
    )
