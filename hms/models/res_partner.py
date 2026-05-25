from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string="Related Patient"
    )

    @api.constrains('email', 'related_patient_id')
    def check_email_not_in_patients(self):
        """Prevent linking customer with email that already exists in patient model"""
        for record in self:
            if record.email:
                # Check if this email exists in patient model
                patient = self.env['hms.patient'].search([
                    ('email', '=', record.email)
                ], limit=1)
                
                if patient and record.related_patient_id != patient:
                    raise ValidationError(
                        f"The email '{record.email}' already exists in the patient records. "
                        f"Cannot link this customer to a different patient."
                    )

    def unlink(self):
        """Prevent deletion of customers linked to patients"""
        for record in self:
            if record.related_patient_id:
                raise ValidationError(
                    f"Cannot delete customer '{record.name}' because it is linked to patient "
                    f"'{record.related_patient_id.first_name} {record.related_patient_id.last_name}'. "
                    f"Please unlink the patient first."
                )
        return super(ResPartner, self).unlink()
