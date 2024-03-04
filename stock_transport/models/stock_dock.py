from odoo import models,fields,api,exceptions

class StockFleet(models.Model):
    _name = "stock.dock"

    name = fields.Char()