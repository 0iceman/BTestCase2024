from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class Complaint(models.Model):
    _name = 'real.estate.complaint'
    _description = 'Real Estate Complaint'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Char(string='Address', required=True, tracking=True)
    complaint_type = fields.Selection([
        ('question', 'Question'),
        ('electrical', 'Electrical Issue'),
        ('heating', 'Heating Issue'),
        ], string='Type of Complaint', required=True, tracking=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
    ('new', 'New'),
    ('in_review', 'In Review'),
    ('in_progress', 'In Progress'),
    ('solved', 'Solved'),
    ('dropped', 'Dropped'),
    ('resolved', 'Resolved')  
    ], string='Status', default='new', tracking=True)

    representative_id = fields.Many2one('res.users', string='Representative')
    complaint_number = fields.Char(string='Complaint Number', readonly=True)
    work_order_number = fields.Char(string='Work Order Number')

    @api.model
    def create(self, vals):
        if not vals.get('complaint_number'):
            vals['complaint_number'] = self.env['ir.sequence'].next_by_code('real.estate.complaint') or _('New')
        vals['representative_id'] = self.env['res.users'].search([], limit=1).id
        complaint = super(Complaint, self).create(vals)
        complaint.activity_schedule(
            'mail.mail_activity_data_todo',
            summary='Complaint Review',
            user_id=complaint.representative_id.id
        )
        template = self.env.ref('real_estate_complaints.email_template_complaint_confirmation')
        template.send_mail(complaint.id, force_send=True)
        return complaint

    def _get_default_representative(self):
        return self.env['res.users'].search([], limit=1).id

    def action_answer_question(self, message):
        self.message_post(body=message)
        self.state = 'resolved'

    def action_dismiss_complaint(self):
        self.write({'state': 'dropped'})   

    def action_send_email_notification(self):
        template = self.env.ref('real_estate_complaints.email_template_complaint_resolution')
        template.send_mail(self.id, force_send=True)
    
    def action_resolve_question(self, response_message):
        if self.complaint_type == 'question':
            self.message_post(body=response_message, subtype='mail.mt_note')
            self.state = 'resolved'

    def action_mark_as_in_review(self):
        """Mark the complaint as 'In Review'."""
        self.write({'state': 'in_review'})

    def action_mark_as_in_progress(self):
        """Mark the complaint as 'In Progress'."""
        self.write({'state': 'in_progress'})

    def action_mark_as_solved(self):
        """Mark the complaint as 'Resolved'."""
        self.write({'state': 'solved'})

    def action_mark_as_dropped(self):
        """Dismiss the complaint."""
        self.write({'state': 'dropped'})
