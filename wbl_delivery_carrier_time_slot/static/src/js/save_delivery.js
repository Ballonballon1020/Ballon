/** @odoo-module **/

import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from '@web/core/network/rpc';


export const websiteSaleDeliverySave = PublicWidget.Widget.extend({
    selector: ".oe_website_sale",
    events: {
        'click [name="website_sale_main_button"]': '_onConfirmClick',
    },

    _onConfirmClick: async function (event) {

        if (window.location.pathname !== "/shop/checkout") {
            return;
        }

        var delivery_date = $('#wbl_delivery_date');
        var delivery_slot = $('#wbl_delivery_slot');
        var delivery_date_val = delivery_date.val();
        var delivery_slot_val = delivery_slot.val();

        $(".delivery-error").remove();

        if (delivery_date_val && delivery_slot_val) {
            const response = await rpc("/save_delivery/", {
            'delivery_date': delivery_date_val,
            'delivery_slot': delivery_slot_val
        });

        if (typeof response !== 'object') {
            console.error("Invalid response from /save_delivery:", response);
            return;
        }
        } else {
            event.preventDefault();

            if (!delivery_date_val) {
                delivery_date.after('<span class="delivery-error text-danger">Please select a delivery date.</span>');
            }
            if (!delivery_slot_val) {
                delivery_slot.after('<span class="delivery-error text-danger">Please select a delivery slot.</span>');
                delivery_slot.css('border', '1px solid #e02b27');
            }
        }
    }
});

PublicWidget.registry.websiteSaleDeliverySave = websiteSaleDeliverySave;
