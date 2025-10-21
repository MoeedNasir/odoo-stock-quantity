# stock_inward_quantity/models/stock_move_line.py
from odoo import models, fields, api, _
from odoo.tools import float_compare

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    # stored so read_group can sum it
    inward_quantity = fields.Float(
        string="Inward Quantity",
        compute="_compute_inward_quantity",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('qty_done', 'quantity', 'location_usage', 'location_dest_usage')
    def _compute_inward_quantity(self):
        """
        Compute stored value = quantity when incoming, else 0.0.
        Note: stock.move.line historically uses qty_done for done moves; keep both checks to be safe.
        """
        for rec in self:
            # determine numeric quantity to consider
            qty = 0.0
            # prefer qty_done (Odoo uses qty_done on move.lines), fallback to quantity
            if hasattr(rec, 'qty_done'):
                qty = float(rec.qty_done or 0.0)
            else:
                qty = float(rec.quantity or 0.0)

            if (rec.location_usage not in ('internal', 'transit')) and (rec.location_dest_usage in ('internal', 'transit')):
                rec.inward_quantity = qty
            else:
                rec.inward_quantity = 0.0

    # override read_group to alter aggregated "quantity" to be sum of inward_quantity
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """
        Call super(). Then, if 'quantity' is one of the aggregated fields,
        replace group['quantity'] with the sum of inward_quantity for that group's domain.
        This affects only group aggregate numbers; individual rows remain unchanged.
        """
        # Call parent to get grouped data
        groups = super(StockMoveLine, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

        # Only proceed if 'quantity' requested and 'inward_quantity' exists (we added it above)
        if 'quantity' in fields:
            # For each returned group, Odoo usually includes a '__domain' key which we can use
            for grp in groups:
                # the group domain to get the records in this group
                grp_domain = grp.get('__domain') or domain
                # read_group to get sum of inward_quantity for this subgroup
                # Requesting no groupby -> aggregated total only
                try:
                    agg = self.env['stock.move.line'].read_group(grp_domain, ['inward_quantity'], [])
                    # read_group returns a list with a single dict for no-groupby
                    if agg and isinstance(agg, list):
                        val = agg[0].get('inward_quantity') or 0.0
                        # Replace the 'quantity' aggregation with inward sum
                        grp['quantity'] = float(val)
                except Exception:
                    # If anything goes wrong, leave grp['quantity'] as returned by super()
                    continue

        return groups
