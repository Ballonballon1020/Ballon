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
from odoo.http import request, route
from datetime import datetime, timedelta
import pytz


class DeliveryTimeSchedule(http.Controller):
    @route('/delivery_schedule', type='jsonrpc', auth='public', website=True)
    def schedule_delivery(self, delivery_id=None):
        if delivery_id:
            delivery_carrier = request.env['delivery.carrier'].search([('id', '=', delivery_id)])
            open_days = []
            for schedule_time in delivery_carrier.time_schedule:
                open_days.append(schedule_time.week_days)
            order = request.cart
            order_delivery_date = order.delivery_date if order and order.delivery_date else None

            if open_days:
                values = {
                    'delivery_date': delivery_carrier.delivery_date,
                    'delivery_slot': delivery_carrier.delivery_time_slot,
                    'start_day_after': delivery_carrier.start_day_after,
                    'open_days': open_days,
                    'order_delivery_date': order_delivery_date,
                    'order_delivery_slot': order.delivery_slot if order else None
                }
                return values
            else:
                values = {
                    'delivery_date': False,
                }
                return values

    @route('/delivery_date', type='jsonrpc', auth='public', website=True)
    def delivery_slot(self, delivery_id=None, delivery_date=None):
        if delivery_id and delivery_date:
            delivery_carrier = request.env['delivery.carrier'].search([('id', '=', delivery_id)])
            order_preparation_time = int(delivery_carrier.order_preparation_time)
            timez_kl = pytz.timezone('Asia/Manila')
            current_date = datetime.now(timez_kl).strftime('%d/%m/%Y')
            now = datetime.now(timez_kl).strftime('%H:%M:%S')
            current_time = datetime.strptime(now, '%H:%M:%S')
            current_time += timedelta(minutes=order_preparation_time)
            current_time = current_time.strftime('%I:%M %p')
            delivery_day = datetime.strptime(delivery_date, '%Y-%m-%d').strftime('%A')
            delivery_slots = self.time_slot(delivery_id, delivery_day)
            html = '<option value="''"' + '>' + 'Choose your delivery slot' + '</option>'
            for key, value in delivery_slots.items():
                slot_booking_status = 'show'
                if current_date == delivery_date and datetime.strptime(current_time,
                                                                       "%I:%M %p").time() > datetime.strptime(key,
                                                                                                              "%I:%M %p").time():
                    slot_booking_status = 'hide'
                else:
                    if self.total_booking_slot(delivery_id, delivery_date,
                                               key + ' to ' + value) >= delivery_carrier.max_order_in_a_slot:
                        slot_booking_status = 'hide'
                if slot_booking_status == 'show':
                    html += '<option value="' + key + ' to ' + value + '"' + '>' + key + ' to ' + value + '</option>'
            values = {
                'delivery_time_slot': delivery_carrier.delivery_time_slot,
                'delivery_slots': html,
                'order_delivery_slot': request.cart.delivery_slot if request.cart else None
            }
            return values
        else:
            values = {'delivery_time_slot': False}
            return values

    @staticmethod
    def time_slot(delivery_id, delivery_day):
        delivery_carrier = request.env['delivery.carrier'].search([('id', '=', delivery_id)])
        interval = delivery_carrier.time_interval
        total_slot = {}
        for schedule_time in delivery_carrier.time_schedule:
            if schedule_time.week_days == delivery_day:

                opening_time = datetime.strptime(schedule_time.open_time_hours + ':' +
                                                 schedule_time.open_time_minutes + ':' + '00', '%H:%M:%S')
                close_hour = int(schedule_time.close_time_hours)
                close_min = int(schedule_time.close_time_minutes)
                if close_hour == 24 and close_min == 0:
                    closing_time = datetime.strptime("00:00:00", "%H:%M:%S") + timedelta(days=1)
                else:
                    closing_time = datetime.strptime(f"{close_hour:02d}:{close_min:02d}:00", "%H:%M:%S")

                difference = opening_time - closing_time
                total_delivery_minutes = abs(difference.total_seconds()) / 60
                time_slot = opening_time
                start = opening_time
                slot = interval
                while slot <= total_delivery_minutes:
                    time_slot += timedelta(minutes=interval)
                    total_slot[start.strftime('%I:%M %p')] = time_slot.strftime('%I:%M %p')
                    start += timedelta(minutes=interval)
                    slot += interval
        return total_slot

    @staticmethod
    def total_booking_slot(delivery_id, delivery_date, delivery_slot):
        count_order = request.env['sale.order'].search_count([
            ('carrier_id', '=', delivery_id),
            ('delivery_date', '=', delivery_date),
            ('delivery_slot', '=', delivery_slot)
        ])
        return count_order
