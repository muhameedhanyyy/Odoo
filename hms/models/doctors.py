from odoo import models, fields


class HMSDoctors(models.Model):
    _name = 'hms.doctors'
    _description = 'HMS Doctors'

    first_name = fields.Char(required=True)

    last_name = fields.Char(required=True)

    image = fields.Binary()
