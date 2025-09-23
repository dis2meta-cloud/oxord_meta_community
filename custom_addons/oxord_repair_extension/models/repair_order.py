from odoo import api, fields, models

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    # Supervisor / workflow fields
    initial_check_by = fields.Many2one('res.users', string="Initial Check By")
    received_date = fields.Datetime(string="Received Date", default=fields.Datetime.now)
    encoded_by = fields.Many2one('res.users', string="Encoded By")
    technician_note = fields.Text(string="Technician Note")
    coordinator_note = fields.Text(string="Coordinator Note")
    bin_location = fields.Char(string="Bin# Location")
    work_order = fields.Char(string="Work Order")

    # Timer relation
    timer_ids = fields.One2many('repair.order.timer', 'order_id', string="Timers", copy=False)

    # Convenience computed aging fields
    initial_check_aging = fields.Char(string="Initial Check Aging", compute='_compute_convenience_aging', store=True)
    received_aging = fields.Char(string="Received Aging", compute='_compute_convenience_aging', store=True)
    endorse_to_tech_aging = fields.Char(string="Endorse to Tech Aging", compute='_compute_convenience_aging', store=True)
    customer_approval_aging = fields.Char(string="Customer Approval Aging", compute='_compute_convenience_aging', store=True)
    parts_request_aging = fields.Char(string="Parts Request Aging", compute='_compute_convenience_aging', store=True)
    end_repair_aging = fields.Char(string="End Repair Aging", compute='_compute_convenience_aging', store=True)

    # Milestone datetime fields
    endorse_to_tech_date = fields.Datetime(string="Endorsed to Tech Date")
    customer_approval_date = fields.Datetime(string="Customer Approval Date")
    parts_request_date = fields.Datetime(string="Parts Request Date")
    end_repair_date = fields.Datetime(string="End Repair Date")
    released_by_occ = fields.Many2one('res.users', string="Released by OCC")
    released_date = fields.Datetime(string="Released Date")

    # Timer actions
    def _get_timer(self, name, create_if_missing=True):
        self.ensure_one()
        timer = self.timer_ids.filtered(lambda t: t.name == name)
        if timer:
            return timer[0]
        if create_if_missing:
            return self.env['repair.order.timer'].create({'order_id': self.id, 'name': name})
        return False

    def action_start_timer(self, name):
        for rec in self:
            rec._get_timer(name).start()
            if name == 'initial_check' and not rec.received_date:
                rec.received_date = fields.Datetime.now()
            if name == 'received' and not rec.received_date:
                rec.received_date = fields.Datetime.now()
            if name == 'endorse_to_tech' and not rec.endorse_to_tech_date:
                rec.endorse_to_tech_date = fields.Datetime.now()
            if name == 'customer_approval' and not rec.customer_approval_date:
                rec.customer_approval_date = fields.Datetime.now()
            if name == 'parts_request' and not rec.parts_request_date:
                rec.parts_request_date = fields.Datetime.now()
            if name == 'end_repair' and not rec.end_repair_date:
                rec.end_repair_date = fields.Datetime.now()

    def action_pause_timer(self, name):
        for rec in self:
            timer = rec._get_timer(name, create_if_missing=False)
            if timer:
                timer.pause()

    def action_resume_timer(self, name):
        for rec in self:
            timer = rec._get_timer(name, create_if_missing=False)
            if timer:
                timer.resume()

    def action_stop_timer(self, name):
        for rec in self:
            timer = rec._get_timer(name, create_if_missing=False)
            if timer:
                timer.stop()
                if name == 'end_repair':
                    rec.end_repair_date = timer.end_dt

    @api.depends('timer_ids.elapsed')
    def _compute_convenience_aging(self):
        for rec in self:
            def get_elapsed(name):
                timer = rec.timer_ids.filtered(lambda t: t.name == name)
                return timer.elapsed if timer else '0s'
            rec.initial_check_aging = get_elapsed('initial_check')
            rec.received_aging = get_elapsed('received')
            rec.endorse_to_tech_aging = get_elapsed('endorse_to_tech')
            rec.customer_approval_aging = get_elapsed('customer_approval')
            rec.parts_request_aging = get_elapsed('parts_request')
            rec.end_repair_aging = get_elapsed('end_repair')
