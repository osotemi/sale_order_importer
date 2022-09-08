# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SaleOrderConfirmationFiles(models.TransientModel):
    _name = "sale.order.confirmation.files"
    _description = ""

    so_confirm_file_data = fields.Binary(string='File')
    so_confirm_file_name = fields.Char(string='Load File Name')

    @api.multi
    def action_apply(self):
        try:
            file_reader_generator = self._import_file_reader()

            for i in file_reader_generator:
                sale_order = self.env['sale.order'].search([('name', '=', i[0])])
                if sale_order and sale_order.state == 'draft':
                    sale_order.write({'state': 'sent'})

        except ValueError:
            raise werkzeug.exceptions.BadRequest('Invalid file format, pleas use .csv, .osd, .xls or .xlsx format')

        return True

    @api.multi
    def _import_file_reader(self):
        """
            Create a base
'       """
