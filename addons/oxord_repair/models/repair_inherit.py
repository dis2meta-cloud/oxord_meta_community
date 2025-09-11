# oxord_repair/models/repair_inherit.py
from odoo import models, fields, api

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    branch_code = fields.Selection(
        selection=[('st4', 'La Hacienda (ST4)'), ('st3', 'Robinsons (ST3)'), ('hq', 'HQ')],
        string='Branch',
        default='st4',
        required=True,
    )
    initial_check_by = fields.Many2one('hr.employee', string='Initial Check By')
    received_date = fields.Datetime(string='Received Date')
    encoded_by = fields.Many2one('res.users', string='Encoded By', default=lambda self: self.env.uid)
    work_order_ref = fields.Char(string='Work Order Ref')
    endorse_to_tech_id = fields.Many2one('hr.employee', string='Endorsed to Technician')
    technician_note = fields.Text(string='Technician Note')
    coordinator_note = fields.Text(string='Coordinator Note')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if not record.work_order_ref:
            seq = self.env['ir.sequence'].next_by_code('oxord.repair.seq') or '/'
            record.work_order_ref = f"OX-{record.branch_code.upper()}-{seq}"
        return record
