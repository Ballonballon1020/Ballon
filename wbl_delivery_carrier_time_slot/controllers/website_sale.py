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

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from datetime import datetime, timedelta


class WebsiteSaleInherit(WebsiteSale):

    @http.route('/save_delivery', type='jsonrpc', auth='public', website=True)
    def save_delivery(self, delivery_date=None, delivery_slot=None):
        if delivery_date or delivery_slot:
            order = request.cart
            if order and order.id:
                dtime = delivery_date + ' ' + delivery_slot.split(' to ')[0]
                dformat = "%Y-%m-%d %I:%M %p"
                date_time = datetime.strptime(dtime, dformat) - timedelta(hours=5, minutes=30)
                order.write({'delivery_date': datetime.strptime(delivery_date, '%Y-%m-%d').date()})
                order.write({'delivery_slot': delivery_slot})
                order.write({'commitment_date': date_time})
                order.write({'expected_date': date_time})
        return {'return': True}
