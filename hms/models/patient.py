from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    first_name = fields.Char(string="First Name")

    last_name = fields.Char(string="Last Name")

    birth_date = fields.Date(string="Birth Date")

    history = fields.Html(string="History")

    cr_ratio = fields.Float(string="CR Ratio")

    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string="Blood Type")

    pcr = fields.Boolean(string="PCR")

    image = fields.Binary(string="Image")

    address = fields.Text(string="Address")

    email = fields.Char(string="Email")

    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        store=True
    )

    department_id = fields.Many2one(
        'hms.department',
        string="Department"
    )

    doctor_ids = fields.Many2many(
        'hms.doctors',
        string="Doctors"
    )

    department_capacity = fields.Integer(
        related='department_id.capacity',
        string="Department Capacity"
    )

    log_ids = fields.One2many(
        'hms.patient.log',
        'patient_id',
        string="Logs"
    )

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ],
        default='undetermined',
        string="State"
    )

    @api.depends('birth_date')
    def _compute_age(self):

        for rec in self:

            if rec.birth_date:

                today = date.today()

                rec.age = (
                    today.year - rec.birth_date.year
                )

            else:

                rec.age = 0

    @api.constrains('department_id')
    def check_department_opened(self):

        for record in self:

            if (
                record.department_id
                and
                not record.department_id.is_opened
            ):

                raise ValidationError(
                    "You cannot choose a closed department."
                )

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):

        for record in self:

            if record.pcr and not record.cr_ratio:

                raise ValidationError(
                    "CR Ratio is mandatory."
                )

    @api.onchange('age')
    def onchange_age(self):

        if self.age and self.age < 30:

            self.pcr = True

            return {

                'warning': {

                    'title': 'Warning',

                    'message':
                        'PCR has been checked automatically'
                }
            }

    def write(self, vals):

        result = super().write(vals)

        if 'state' in vals:

            for record in self:

                self.env['hms.patient.log'].create({

                    'patient_id': record.id,

                    'description':
                        f"State changed to {record.state}"
                })

        return result

    @api.constrains('email')
    def check_email_valid(self):
        for record in self:
            if record.email:
                # Basic email validation
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, record.email):
                    raise ValidationError(
                        "Please enter a valid email address."
                    )

    _unique_email = models.Constraint(
        'UNIQUE(email)',
        'This email address already exists in the patient records!'
    )
