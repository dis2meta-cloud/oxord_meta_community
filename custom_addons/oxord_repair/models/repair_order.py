from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    # ------------------------
    # Branch Field
    # ------------------------
    branch = fields.Selection(
        [
            ('hq', 'Headquarters'),
            ('la_hacienda', 'La Hacienda'),
            ('robinsons', 'Robinsons')
        ],
        string='Branch',
        default='la_hacienda',
        required=True,
        help="Select the branch for this repair order"
    )

    # ------------------------
    # Override create method to assign branch-specific sequence
    # ------------------------
    @api.model
    def create(self, vals):
        branch = vals.get('branch', 'la_hacienda')  # default if not set

        # Prevent repair orders for HQ
        if branch == 'hq':
            raise UserError("Repair orders cannot be created for HQ branch.")

        # Force branch-specific sequence
        if branch == 'la_hacienda':
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.order.lahacienda')
        elif branch == 'robinsons':
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.order.robinsons')
        else:
            # Fallback default sequence
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.order') or '/'

        return super(RepairOrder, self).create(vals)


    # ------------------------
    # Additional Fields
    # ------------------------
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        readonly=False,
        index=True
    )
    schedule_date = fields.Datetime(string="Scheduled Date")
    component_status = fields.Selection([
        ('ok', 'OK'),
        ('for_replacement', 'For Replacement'),
        ('defective', 'Defective')
    ], string="Component Status")
    initial_check_by = fields.Many2one('res.users', string="Initial Check By")
    received_date = fields.Datetime(string="Received Date", default=fields.Datetime.now)
    received_aging = fields.Char(string="Received Aging", compute="_compute_received_aging", store=True)
    initial_check_aging = fields.Char(string="Initial Check Aging", compute="_compute_initial_check_aging", store=True)
    encoded_by = fields.Many2one('res.users', string="Encoded By")
    encoded_aging = fields.Char(string="Encoded Aging", compute="_compute_encoded_aging", store=True)
    work_order = fields.Char(string="Work Order")
    endorse_to_tech = fields.Many2one('res.users', string="Endorsed to Tech")
    endorse_to_tech_aging = fields.Char(string="Endorse to Tech Aging", compute="_compute_endorse_to_tech_aging", store=True)
    endorse_to_authorized_coordinator = fields.Many2one('res.users', string="Endorsed to Authorized Coordinator")
    endorse_to_authorized_coordinator_aging = fields.Char(string="Coordinator Aging", compute="_compute_endorse_to_authorized_coordinator_aging", store=True)

    # ------------------------
    # Aging Computation Helper
    # ------------------------
    def _format_duration(self, start_time):
        if not start_time:
            return ''
        now = datetime.now()
        diff = now - start_time
        seconds = int(diff.total_seconds())
        years, remainder = divmod(seconds, 31536000)
        months, remainder = divmod(remainder, 2592000)
        days, remainder = divmod(remainder, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{years}y, {months}m, {days}d, {hours}h, {minutes}min, {seconds}s"

    @api.depends('received_date')
    def _compute_received_aging(self):
        for rec in self:
            rec.received_aging = self._format_duration(rec.received_date)

    @api.depends('received_date', 'initial_check_by')
    def _compute_initial_check_aging(self):
        for rec in self:
            rec.initial_check_aging = self._format_duration(rec.received_date) if rec.initial_check_by else ''

    @api.depends('received_date', 'encoded_by')
    def _compute_encoded_aging(self):
        for rec in self:
            rec.encoded_aging = self._format_duration(rec.received_date) if rec.encoded_by else ''

    @api.depends('received_date', 'endorse_to_tech')
    def _compute_endorse_to_tech_aging(self):
        for rec in self:
            rec.endorse_to_tech_aging = self._format_duration(rec.received_date) if rec.endorse_to_tech else ''

    @api.depends('received_date', 'endorse_to_authorized_coordinator')
    def _compute_endorse_to_authorized_coordinator_aging(self):
        for rec in self:
            rec.endorse_to_authorized_coordinator_aging = self._format_duration(rec.received_date) if rec.endorse_to_authorized_coordinator else ''

    # ------------------------
    # Parts Request Action
    # ------------------------
    def action_open_parts_request(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Parts Request',
            'res_model': 'repair.parts.request',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_repair_id': self.id,
            }
        }
