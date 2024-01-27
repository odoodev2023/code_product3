from odoo import models, fields, api

class CategoryInherit(models.Model):
    _inherit = 'product.category'

    code = fields.Char(string="Code", size=5)
    sequence_id = fields.Many2one('ir.sequence', string='Sequence')


    @api.model
    def generate_sequence(self, category_name):
        sequence_code = f'category_{category_name}_sequence'
        sequence = self.env['ir.sequence'].create({
            'name': sequence_code,
            'code': sequence_code,
            'padding': 3,
        })



        return sequence.id

class ProductInherit(models.Model):
    _inherit = 'product.product'

    code_id = fields.Char(string="Code Id", related='categ_id.code')

    @api.model
    def create(self, vals):
        if 'categ_id' in vals:
            category = self.env['product.category'].browse(vals['categ_id'])
            code_details = str(category.code)
            sequence_number = str(category.sequence_id.next_by_id())

            vals['default_code'] = code_details + sequence_number

        return super(ProductInherit, self).create(vals)
