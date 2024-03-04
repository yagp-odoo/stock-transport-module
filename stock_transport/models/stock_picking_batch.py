from odoo import models,fields,api,exceptions

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock = fields.Many2one('stock.dock', string="Dock")
    vehicle = fields.Many2one('fleet.vehicle', placeholder="3rd Party Provider")
    vehicle_category = fields.Many2one('fleet.vehicle.model.category', placeholder="e.g. Semi-Truck")
    weight = fields.Float(compute="_compute_weight", store=True)
    weight_progress = fields.Float(compute="_compute_weight_progress", string="Weight")
    volume = fields.Float(compute="_compute_volume", store=True)
    volume_progress = fields.Float(compute="_compute_volume_progress", string="Volume")

    @api.depends('move_line_ids.product_id.weight', 'vehicle_category.max_weight')
    def _compute_weight(self):
        for rec in self:
            rec.weight = sum(line.product_id.weight for line in rec.move_line_ids)

    @api.depends('vehicle_category.max_weight','weight')
    def _compute_weight_progress(self):
        for rec in self:
            if rec.weight and rec.vehicle_category.max_weight:
                progress1 = rec.weight / rec.vehicle_category.max_weight * 100
            else:
                progress1 = 0
            rec.weight_progress = progress1
            
    @api.depends('move_line_ids.product_id.volume', 'vehicle_category.max_volume')
    def _compute_volume(self):
        for rec in self:
            rec.volume = sum(line.product_id.volume for line in rec.move_line_ids)


    @api.depends('vehicle_category.max_weight','volume')
    def _compute_volume_progress(self):
        for rec in self:
            if rec.volume and rec.vehicle_category.max_volume:
                progress2 = rec.volume / rec.vehicle_category.max_volume * 100
            else:
                progress2 = 0
            rec.volume_progress = progress2