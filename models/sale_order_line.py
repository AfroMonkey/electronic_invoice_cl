# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _action_procurement_create(self):
        """
        Create procurements based on quantity ordered. If the quantity is increased, new
        procurements are created. If the quantity is decreased, no automated action is taken.
        """
        # HomebrewSoft Modified
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        new_procs = self.env['procurement.order']  # Empty recordset
        for line in self:
            if line.state != 'sale' or not line.product_id._need_procurement():
                continue
            qty = 0.0
            for proc in line.procurement_ids.filtered(lambda r: r.state != 'cancel'):
                qty += proc.product_qty
            if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
                continue
            if not line.order_id.procurement_group_id:
                vals = line.order_id._prepare_procurement_group()
                line.order_id.procurement_group_id = self.env["procurement.group"].create(vals)

            vals = line._prepare_order_line_procurement(group_id=line.order_id.procurement_group_id.id)
            vals['price_unit'] = line.price_unit  # HomebrewSoft Modification
            vals['product_qty'] = line.product_uom_qty - qty  # HomebrewSoft Modification
            new_proc = self.env["procurement.order"].with_context(procurement_autorun_defer=True).create(vals)
            new_proc.write({  # HomebrewSoft Modification
                'tax_ids': [(6, 0, line.tax_id.ids)],  # HomebrewSoft Modification
            })  # HomebrewSoft Modification
            new_proc.message_post_with_view('mail.message_origin_link',
                                            values={'self': new_proc, 'origin': line.order_id},
                                            subtype_id=self.env.ref('mail.mt_note').id)
            new_procs += new_proc
        new_procs.run()
        return new_procs
