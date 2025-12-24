# -*- coding: utf-8 -*-
#
#################################################################################
# Author      : Weblytic Labs Pvt. Ltd. (<https://store.weblyticlabs.com/>)
# Copyright(c): 2023-Present Weblytic Labs Pvt. Ltd.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
##################################################################################

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = 'Sale Order'

    delivery_date = fields.Date('Delivery Date')
    delivery_slot = fields.Char('Delivery Slot')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.delivery_date:
            for rec in self.picking_ids:
                rec.write({'scheduled_date': self.commitment_date})
                rec.write({'date_deadline': self.commitment_date})
                rec.write({'delivery_slot': self.delivery_slot})
        return res
