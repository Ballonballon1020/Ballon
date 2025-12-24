/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { renderToElement } from "@web/core/utils/render";
import { KeepLast } from "@web/core/utils/concurrency";
import { Component } from "@odoo/owl";
import { DatePicker } from "@web/core/datetime/datetime_picker"
import { rpc } from '@web/core/network/rpc';

publicWidget.registry.websiteSaleDeliveryTimeSlot = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
        events: {
            'click [name="o_delivery_method"]': '_onCarrierClick',
            'change #wbl_delivery_date': '_onDeliveryDateChange',
        },

    init() {
        this._super(...arguments);
    },
    start() {
       const selectedCarrierInput = this.$('[name="o_delivery_radio"]:checked');
        if (selectedCarrierInput.length) {
           this._onCarrierClick({ currentTarget: selectedCarrierInput[0] });
        }
    },

    /**
     * @private
     * @param {Event} ev
     */
    _onCarrierClick: async function (ev) {

        var delivery_id = ev.currentTarget.querySelector('input[type="radio"]');
        if (delivery_id  === null ){
            var delivery_id = ev.currentTarget
        }
        $('#wbl_delivery_date').datepicker("destroy");
        await rpc("/delivery_schedule", {
            delivery_id: parseInt(delivery_id.dataset.dmId),
        }).then((response) => {
            if(response.delivery_date == true) {
                var today = new Date();
                var start_day_after = response.start_day_after * 24;
                var allowedDays = response.open_days;

                var weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                var tomorrow = new Date(today.getTime() + start_day_after * 60 * 60 * 1000);
                while (!allowedDays.includes(weekday[tomorrow.getDay()])) {
                    tomorrow.setDate(tomorrow.getDate() + 1);
                }
                if (response.order_delivery_date){
                    $("#wbl_delivery_date").datepicker({
                dateFormat: "yy-mm-dd",
                minDate: tomorrow,
                autoHide: true,
                beforeShowDay: function (date) {
                    var currentDay = weekday[date.getDay()];
                    if (response.delivery_slot == true) {
                        if (allowedDays.includes(currentDay)) {
                            return [true, ''];
                        } else {
                            return [false, ''];
                        }
                    } else {
                        return [true, ''];
                    }
                },
		        }).datepicker('setDate', response.order_delivery_date);
		        } else{
		            $("#wbl_delivery_date").datepicker({
                dateFormat: "yy-mm-dd",
                minDate: tomorrow,
                autoHide: true,
                beforeShowDay: function (date) {
                    var currentDay = weekday[date.getDay()];
                    if (response.delivery_slot == true) {
                        if (allowedDays.includes(currentDay)) {
                            return [true, ''];
                        } else {
                            return [false, ''];
                        }
                    } else {
                        return [true, ''];
                    }
                },
		        }).datepicker('setDate', tomorrow);
		        }

                $('#schedule_delivery').show();
				$('#wbl_delivery_date').attr('data-delivery-id', parseInt(delivery_id.dataset.dmId));
                rpc("/delivery_date", {
                    delivery_date: $('#wbl_delivery_date').val(),
                    delivery_id: parseInt(delivery_id.dataset.dmId),
                }).then((response) => {
                    if (response.delivery_time_slot == true && response.delivery_slots != '') {
                        $('#wbl_delivery_slot').empty();
                        $('#wbl_delivery_slot').append(response.delivery_slots);
                        $('#wbl_slot_group').show();

                        // Preselect the order's existing delivery slot
                        if (response.order_delivery_slot) {
                            $('#wbl_delivery_slot').val(response.order_delivery_slot);
                        }
                    } else {
                        $('#wbl_slot_group').hide();
                    }
                });
            } else {
                $('#schedule_delivery').hide();
            }
        });
    },

    _onDeliveryDateChange: async function (ev) {
        var date = ev.target.value;
        console.log(ev.target);
        var $input = $(ev.currentTarget);
		var delivery_id = $input.attr('data-delivery-id');
        rpc("/delivery_date", {
            delivery_date: date,
            delivery_id: parseInt(delivery_id),
        }).then((response) => {
            if(response.delivery_time_slot == true && response.delivery_slots != '') {
                $('#wbl_delivery_slot').empty();
                $('#wbl_delivery_slot').append(response.delivery_slots);
                $('#wbl_slot_group').show();
                $('#wbl_delivery_date').css('border', '');
                $('#wbl-error-message-date').text('').css('color', '');
            } else {
                $('#wbl_slot_group').hide();
                $('#wbl_delivery_date').css('border', '1px solid #e02b27');
            }
        });
    },

});
