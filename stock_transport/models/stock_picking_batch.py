from odoo import models, fields, api
from datetime import datetime, timedelta
import base64

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one('stock.dock', string="Dock")
    vehicle_id = fields.Many2one('fleet.vehicle', placeholder="3rd Party Provider")
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', placeholder="e.g. Semi-Truck")
    weight = fields.Float(compute="_compute_weight", store=True)
    weight_progress = fields.Float(compute="_compute_weight_progress", string="Weight")
    volume = fields.Float(compute="_compute_volume", store=True)
    volume_progress = fields.Float(compute="_compute_volume_progress", string="Volume")
    transfer_count = fields.Integer(compute="_compute_transfer_count", store=True)
    lines_count = fields.Integer(compute="_compute_lines_count", store=True)

    @api.depends('weight', 'volume')
    def _compute_display_name(self):
        for rec in self:
            rounded_weight = round(rec.weight, 3)
            rounded_volume = round(rec.volume, 3)
            driver_text = "No driver" 

            if rec.vehicle_id and rec.vehicle_id.driver_id:
                driver_text = f"Driver: {rec.vehicle_id.driver_id.name} ✅"

            rec.display_name = f"{rec.name}: {rounded_weight}kg, {rounded_volume}m³ ({driver_text})"

        return True

    @api.depends('picking_ids')
    def _compute_transfer_count(self):
        for rec in self:
            rec.transfer_count = len(rec.picking_ids)

    @api.depends('move_line_ids')
    def _compute_lines_count(self):
        for rec in self:
            rec.lines_count = len(rec.move_line_ids)


    @api.depends('move_line_ids.product_id.weight', 'move_line_ids.quantity', 'vehicle_category_id.max_weight')
    def _compute_weight(self):
        for rec in self:
            rec.weight = sum(line.product_id.weight * line.quantity for line in rec.move_line_ids)

    @api.depends('vehicle_category_id.max_weight', 'weight')
    def _compute_weight_progress(self):
        for rec in self:
            if rec.weight and rec.vehicle_category_id.max_weight:
                progress1 = rec.weight / rec.vehicle_category_id.max_weight * 100
            else:
                progress1 = 0
            rec.weight_progress = progress1

    @api.depends('move_line_ids.product_id.volume', 'move_line_ids.quantity', 'vehicle_category_id.max_volume')
    def _compute_volume(self):
        for rec in self:
            rec.volume = sum(line.product_id.volume * line.quantity for line in rec.move_line_ids)

    @api.depends('vehicle_category_id.max_weight', 'volume')
    def _compute_volume_progress(self):
        for rec in self:
            if rec.volume and rec.vehicle_category_id.max_volume:
                progress2 = rec.volume / rec.vehicle_category_id.max_volume * 100
            else:
                progress2 = 0
            rec.volume_progress = progress2
