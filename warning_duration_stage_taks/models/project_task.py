from odoo import models, fields, api
from datetime import datetime

class ProjectTask(models.Model):
    _inherit = ['project.task']

    stage_duration_hours = fields.Float(
        string='Stage Duration Hours',
        compute='_compute_stage_duration_hours',
        readonly=False
    )

    stage_duration_icon = fields.Selection(
        [('normal', 'Normal'), ('warning', 'Warning'), ('danger', 'Danger')],
        string='Stage Duration Icon',
        compute='_compute_stage_duration_icon'
    )

    def _compute_stage_duration_hours(self):
        today = fields.Date.context_today(self)
        for task in self:
            if task.charge_date:
                record_date = fields.Date.from_string(task.charge_date)
    
                if task.stage_id and record_date > today:
                    if task.stage_id and task.date_last_stage_update:
                        duration = datetime.now() - task.date_last_stage_update
                        task.stage_duration_hours = duration.total_seconds() / 3600
                    else:
                        task.stage_duration_hours = 0.0

    def _compute_stage_duration_icon(self):
        for task in self:
            if task.stage_duration_hours < 48 and task.stage_duration_hours > 24:
                task.stage_duration_icon = 'warning'
            elif task.stage_duration_hours > 48:
                task.stage_duration_icon = 'danger'
            else :
                task.stage_duration_icon = 'normal'


    @api.model
    def create(self, vals):
        vals['date_last_stage_update'] = fields.Datetime.now()
        return super(ProjectTask, self).create(vals)

    def write(self, vals):
        if 'stage_id' in vals:
            vals['date_last_stage_update'] = fields.Datetime.now()
        return super(ProjectTask, self).write(vals)

    date_last_stage_update = fields.Datetime(string='Last Stage Update Date', readonly=False)

    @api.model
    def update_stage_duration(self):
        tasks = self.search([])
        for task in tasks:
            task._compute_stage_duration_hours()
