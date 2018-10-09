from odoo import models, fields, api

SELECTION_INFORMATION = [
    ("N", "N - No transmitted information"),
    ("A", "A - Aural telegraphy, intended to be decoded by ear, such as Morse code"),
    ("B", "B - Electronic telegraphy, intended to be decoded by machine (radioteletype and digital modes)"),
    ("C", "C - Facsimile (still images)"),
    ("D", "D - Data transmission, telemetry or telecommand (remote control)"),
    ("E", "E - Telephony (voice or music intended to be listened to by a human)"),
    ("F", "F - Video (television signals)"),
    ("W", "W - Combination of any of the above"),
    ("X", "X - None of the above")
]

SELECTION_SIGNAL = [
    ("0", "0 - No modulating signal"),
    ("1", "1 - One channel containing digital information, no subcarrier"),
    ("2", "2 - One channel containing digital information, using a subcarrier"),
    ("3", "3 - One channel containing analog information"),
    ("7", "7 - More than one channel containing digital information"),
    ("8", "8 - More than one channel containing analog information"),
    ("9", "9 - Combination of analog and digital channels"),
    ("X", "X - None of the above")
]

SELECTION_MODULATION = [
    ("N", "N - Unmodulated carrier"),
    ("A", "A - Double-sideband amplitude modulation (e.g. AM broadcast radio)"),
    ("H", "H - Single-sideband with full carrier (e.g. as used by CHU)"),
    ("R", "R - Single-sideband with reduced or variable carrier"),
    ("J", "J - Single-sideband with suppressed carrier (e.g. Shortwave utility and amateur stations)"),
    ("B", "B - Independent sideband (two sidebands containing different signals)"),
    ("C", "C - Vestigial sideband (e.g. NTSC)"),
    ("F", "F - Frequency modulation (e.g. FM broadcast radio)"),
    ("G", "G - Phase modulation"),
    ("D", "D - Combination of AM and FM or PM"),
    ("P", "P - Sequence of pulses without modulation"),
    ("K", "K - Pulse amplitude modulation"),
    ("L", "L - Pulse width modulation (e.g. as used by WWVB)"),
    ("M", "M - Pulse position modulation"),
    ("Q", "Q - Sequence of pulses, phase or frequency modulation within each pulse"),
    ("V", "V - Combination of pulse modulation methods"),
    ("W", "W - Combination of any of the above"),
    ("X", "X - None of the above")
]


class Modulation(models.Model):
    _name = "stationlog.modulation"
    _description = "Modulation"
    _order = "name ASC"
    _rec_name = "complete_name"

    _constraints = [
        ("name_uniq", "UNIQUE(name)", "Modulation already exists. Name must be unique.")
    ]

    name = fields.Char(
        string="Name",
        required=True,
        translate=False,
    )

    complete_name = fields.Char(
        string="Complete name",
        translate=False,
        compute="_compute_complete_name",
        store=True
    )

    modulation = fields.Selection(
        string="Modulation",
        required=True,
        selection=SELECTION_MODULATION
    )

    signal = fields.Selection(
        string="Signal",
        required=True,
        selection=SELECTION_SIGNAL
    )

    information = fields.Selection(
        string="Information",
        required=True,
        selection=SELECTION_INFORMATION
    )

    emission = fields.Char(
        string="Emission",
        compute="_compute_emission",
        translate=False
    )

    note = fields.Html(
        string="Note"
    )

    @api.depends("emission", "name")
    def _compute_complete_name(self):
        for rec in self:
            rec.complete_name = "%s (%s)" % (rec.name, rec.emission)

    @api.depends("modulation", "signal", "information")
    def _compute_emission(self):
        for rec in self:
            rec.emission = self._emission_string(rec.modulation, rec.signal, rec.information)

    @staticmethod
    def _emission_string(m, s, i):
        return "%s%s%s" % (m, s, i)
