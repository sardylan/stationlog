odoo.define('widget_datetime_tz.basic_fields', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var fields = require('web.basic_fields');

    var FieldDateTimeTZ = fields.FieldDateTime.extend({
        supportedFieldTypes: ['datetime'],

        init: function () {
            this._super.apply(this, arguments);
            this.formatOptions.timezone = false;
            if (this.value) {
                // var offset = this.getSession().getTZOffset(this.value);
                var offset = 0;
                var displayedValue = this.value.clone().add(offset, 'minutes');
                this.datepickerOptions.defaultDate = displayedValue;
            }
        },
        _getValue: function () {
            var value = this.datewidget.getValue();
            // var offset = -this.getSession().getTZOffset(value);
            var offset = 0;
            return value && value.add(offset, 'minutes');
        },
        _renderEdit: function () {
            // var offset = this.getSession().getTZOffset(this.value);
            var offset = 0;
            var value = this.value && this.value.clone().add(offset, 'minutes');
            this.datewidget.setValue(value);
            this.$input = this.datewidget.$input;
        },
    });

    registry.add('datetime_tz', FieldDateTimeTZ);

    return {
        FieldDateTimeTZ: FieldDateTimeTZ
    };

});
