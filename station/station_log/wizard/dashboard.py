from odoo import models, fields, api


class Dashboard(models.TransientModel):
    _name = "station_log.wizard_dashboard"
    _description = "Main dashboard with QSOs summary"

    logbook_id = fields.Many2one(
        string="Logbook",
        comodel_name="station_log.logbook",
        domain=lambda self: self.domain_logbook_id(),
        default=lambda self: self.default_logbook_id()
    )

    qso_count = fields.Integer(
        string="QSO count",
        help="Number of total QSO in logbook",
        compute="_compute_data",
        readonly=True
    )

    country_count = fields.Integer(
        string="Country count",
        help="Number of unique countries in logbook",
        compute="_compute_data",
        readonly=True
    )

    modulation_qso_count_ids = fields.One2many(
        string="Per modulation",
        help="Number of QSO per modulation",
        comodel_name="station_log.wizard_dashboard_qso_modulation_count",
        inverse_name="wizard_id",
        readonly=True
    )

    def domain_logbook_id(self):
        return [
            ("active", "=", True),
            ("res_users_ids", "in", [self.env.uid])
        ]

    def default_logbook_id(self):
        logbook_obj = self.env["station_log.logbook"]
        logbook_domain = self.domain_logbook_id()
        logbook_id = logbook_obj.search(logbook_domain, limit=1)
        if not logbook_id:
            return False

        return logbook_id.id

    @api.depends("logbook_id")
    def _compute_data(self):
        self.ensure_one()

        if not self.logbook_id:
            return

        qso_obj = self.env["station_log.qso"]
        qso_modulation_count_obj = self.env["station_log.wizard_dashboard_qso_modulation_count"]

        self.qso_count = qso_obj.search([
            ("logbook_id.id", "=", self.logbook_id.id)
        ], count=True)

        self._cr.execute(
            "SELECT m.id AS modulation_id, "
            "  count(q.id) AS qso_count "
            "FROM station_log_qso q "
            "  INNER JOIN hamutility_modulation m ON q.modulation_id = m.id "
            "GROUP BY m.id "
            "ORDER BY qso_count DESC "
            "LIMIT 10;"
        )

        qso_modulation_countids = [(5, False)]
        for result in self._cr.fetchall():
            vals = {
                "wizard_id": self.id,
                "logbook_id": self.logbook_id.id,
                "modulation_id": result[0],
                "qso_count": result[1]
            }

            qso_modulation_count_id = qso_modulation_count_obj.create(vals)
            qso_modulation_countids.append((4, qso_modulation_count_id.id))

        self.modulation_qso_count_ids = qso_modulation_countids


class DashboardQsoModulationCount(models.TransientModel):
    _name = "station_log.wizard_dashboard_qso_modulation_count"
    _description = "Helper transient model for dashboard"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="station_log.wizard_dashboard"
    )

    logbook_id = fields.Many2one(
        string="Logbook",
        comodel_name="station_log.logbook"
    )

    modulation_id = fields.Many2one(
        stirng="Modulation",
        help="Modulation",
        comodel_name="hamutility.modulation"
    )

    qso_count = fields.Integer(
        string="QSO count",
        help="QSO count",
        readonly=True
    )

    def action_open(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "QSO in %s" % self.modulation_id.complete_name,
            "res_model": "station_log.qso",
            "view_mode": "tree,form",
            "target": "main",
            "domain": [
                ("logbook_id", "=", self.logbook_id.id),
                ("modulation_id", "=", self.modulation_id.id)
            ]
        }
