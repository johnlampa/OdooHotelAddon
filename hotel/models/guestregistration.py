from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Hotel Guest Registration'

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")
    roomname = fields.Char("Room No.", related='room_id.name')
    roomtname = fields.Char("Room Type", related='room_id.roomtypename')
    guestname = fields.Char("Guest Name", related='guest_id.name')
    datecreated = fields.Date("Date Created", default=lambda self: fields.Date.today())
    datefromSched = fields.Date("Scheduled Check In")
    datetoSched = fields.Date("Scheduled Check Out")
    datefromAct = fields.Date("Actual Check In")
    datetoAct = fields.Date("Actual Check Out")
    name = fields.Char("Guest Registration", compute='_compute_name', store=True)
    state = fields.Selection([
        ('DRAFT', 'Draft'),
        ('RESERVED', 'Reserved'),
        ('CHECKEDIN', 'Checked In'),
        ('CHECKEDOUT', 'Checked Out'),
        ('CANCELLED', 'Cancelled')
    ], string="Status", default="DRAFT")

    @api.depends('room_id', 'guest_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.roomname}, {rec.guestname}"

    def action_reserve(self):
        for rec in self:
            if not rec.guest_id:
                raise ValidationError('Please supply a valid guest.')
            elif not rec.roomname:
                raise ValidationError('Please supply a valid Room Number.')
            else:
                rec.state = "RESERVED"

    def action_checkin(self):
        for rec in self:
            rec.state = "CHECKEDIN"

    def action_checkout(self):
        for rec in self:
            rec.state = "CHECKEDOUT"

    def action_cancel(self):
        for rec in self:
            rec.state = "CANCELLED"