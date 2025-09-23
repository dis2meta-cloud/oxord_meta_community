from odoo import api, fields, models

class RepairOrderTimer(models.Model):
    _name = 'repair.order.timer'
    _description = 'Repair Order Timer'

    order_id = fields.Many2one('repair.order', string="Repair Order", required=True, ondelete='cascade')
    name = fields.Char(string="Timer Name", required=True)
    start_dt = fields.Datetime(string="Start Date")
    end_dt = fields.Datetime(string="End Date")
    elapsed = fields.Char(string="Elapsed Time", compute='_compute_elapsed', store=True)

    @api.depends('start_dt', 'end_dt')
    def _compute_elapsed(self):
        for rec in self:
            if rec.start_dt and rec.end_dt:
                delta = rec.end_dt - rec.start_dt
                rec.elapsed = str(delta)
            else:
                rec.elapsed = '0:00:00'

    def start(self):
        for rec in self:
            rec.start_dt = fields.Datetime.now()
            rec.end_dt = False

    def pause(self):
        for rec in self:
            if rec.start_dt:
                rec.end_dt = fields.Datetime.now()

    def resume(self):
        for rec in self:
            if rec.end_dt:
                delta = rec.end_dt - rec.start_dt
                rec.start_dt = fields.Datetime.now() - delta
                rec.end_dt = False

    def stop(self):
        for rec in self:
            if rec.start_dt:
                rec.end_dt = fields.Datetime.now()
