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

    altitude = fields.Integer(
        string="Altitude",
        help="Altitude",
        track_visibility="onchange"
    )

    position = fields.Char(
        string="Position",
        help="Location position",
        required=True,
        default=lambda self: self.env["widget_googlemaps.utility_googlemaps"].compute_default_position_value()
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

    latitude = fields.Float(
        string="Latitude",
        help="Latitude",
        digits=(9, 6),
        readonly=True,
        compute="compute_coordinates"
    )

    longitude = fields.Float(
        string="Longitude",
        help="Longitude",
        digits=(9, 6),
        readonly=True,
        compute="compute_coordinates"
    )

    def compute_coordinates(self):
        googlemaps_utility = self.env["widget_googlemaps.utility_googlemaps"]

        for rec in self:
            latitude, longitude = googlemaps_utility.get_coordinates_from_position(rec.position)
            rec.latitude = latitude
            rec.longitude = longitude


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
