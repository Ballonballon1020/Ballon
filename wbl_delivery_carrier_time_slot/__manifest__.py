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

{
    'name': 'Delivery Date Picker and Time Slots',
    'version': '19.0.1.0.0',
    'summary': """Delivery date calendar and time, Delivery date scheduler, Schedule delivery date and time, Delivery date/time scheduler, Delivery scheduling system, Delivery date picker, Delivery time slots, Delivery preference selection, Delivery preference selection, Scheduled delivery options, Time slot selection, Shipping methods, Customizable delivery options, Flexible delivery scheduling, Delivery time picker, Delivery Slot Customization, Shipping schedule, Dynamic delivery planning, Delivery schedule optimization, Customizable delivery calendar, Order delivery scheduling, Delivery schedule management, Delivery date picker and time slot.""",
    'description': """Delivery date calendar and time, Delivery date scheduler, Schedule delivery date and time, Delivery date/time scheduler, Delivery scheduling system, Delivery date picker, Delivery time slots, Delivery preference selection, Delivery preference selection, Scheduled delivery options, Time slot selection, Shipping methods, Customizable delivery options, Flexible delivery scheduling, Delivery time picker, Delivery Slot Customization, Shipping schedule, Dynamic delivery planning, Delivery schedule optimization, Customizable delivery calendar, Order delivery scheduling, Delivery schedule management, Delivery date picker and time slot.""",
    'category': 'eCommerce',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': "https://store.weblyticlabs.com",
    'price': '35.00',
    'currency': 'USD',
    'depends': ['base', 'mail', 'website', 'website_sale', 'delivery', 'mrp', 'stock', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_carrier_views.xml',
        'views/stock_picking_views.xml',
        'views/sale_order_views.xml',
        'views/website_sale_delivery_templates.xml',
        'views/sale_portal_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'wbl_delivery_carrier_time_slot/static/src/js/jquery-migrate.js',
            'wbl_delivery_carrier_time_slot/static/src/js/delivery_time_slot.js',
            'wbl_delivery_carrier_time_slot/static/src/js/datepicker.js',
            'wbl_delivery_carrier_time_slot/static/src/js/save_delivery.js',
            'wbl_delivery_carrier_time_slot/static/src/css/datepicker.css',
            'wbl_delivery_carrier_time_slot/static/src/css/deliverytime.css',
        ],
    },
    'images': ['static/description/banner.gif'],
    'live_test_url': 'https://youtu.be/F8QjgcfA0I4',
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
