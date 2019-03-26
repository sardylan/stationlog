import logging

from odoo import models

_logger = logging.getLogger(__name__)


class QSOToolsWizard(models.TransientModel):
    _name = "awards_naval.wizard_qso_tools"

    def action_update_reference_auto(self):
        qso_obj = self.env["award_naval.qso"]
        qso_obj.action_update_reference_auto()

    def action_update_missing_reference(self):
        qso_obj = self.env["award_naval.qso"]
        qso_obj.action_update_missing_reference()

    def action_compute_dupe(self):
        qso_obj = self.env["award_naval.qso"]
        qso_obj.action_compute_dupe()
