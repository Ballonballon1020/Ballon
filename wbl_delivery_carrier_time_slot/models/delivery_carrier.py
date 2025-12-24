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


class ProductTemplate(models.Model):
    _inherit = 'delivery.carrier'

    delivery_date = fields.Boolean('Delivery Date', default=True)
    delivery_time_slot = fields.Boolean('Delivery Time Slot', default=True)
    start_day_after = fields.Integer('Start After (x) Days', default=0)
    order_preparation_time = fields.Selection(
        selection='_get_order_preparation_minutes',
        string='Order Preparation Time'
    )
    time_interval = fields.Integer('Time Interval (Minutes)', default=60)
    max_order_in_a_slot = fields.Integer('Maximum Order in Single Slot', default=10)
    time_schedule = fields.One2many(
        'delivery.time.schedule',
        inverse_name='delivery_carrier_id',
        string='Time Schedule'
    )

    @staticmethod
    def _get_order_preparation_minutes():
        return [
            ('15', '15 minutes'),
            ('30', '30 minutes'),
            ('45', '45 minutes'),
            ('60', '60 minutes'),
            ('75', '75 minutes'),
            ('90', '90 minutes'),
            ('120', '120 minutes'),
            ('180', '180 minutes'),
        ]
