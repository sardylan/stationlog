odoo.define('widget_googlemaps.googlemaps', function (require) {
    'use strict';

    let DebouncedField = require('web.basic_fields').DebouncedField;
    let registry = require('web.field_registry');

    let GoogleMaps = DebouncedField.extend({
        className: 'googlemaps',
        tagName: 'div',
        supportedFieldTypes: ['char'],

        start: function () {
            let options = this.attrs.options;

            let mapDiv = $('<div>');
            mapDiv.addClass('googlemaps-map');
            $(this.el).append(mapDiv);

            if (!('center' in options)) options.center = {lat: 0, lng: 0};
            if (!('zoom' in options)) options.zoom = 4;
            if (!('mapTypeId' in options)) options.mapTypeId = 'hybrid';

            if (!('mode' in options)) options.mode = 'locator';

            this.map = new google.maps.Map(mapDiv[0], {
                center: options.center,
                zoom: options.zoom,
                mapTypeId: options.mapTypeId
            });

            switch (options.mode) {
                case 'marker':
                    this.marker = new google.maps.Marker({
                        position: {lat: 0, lng: 0},
                        title: '',
                        draggable: false,
                        map: this.map
                    });

                    break;

                case 'rectangle':
                    this.rectangle = new google.maps.Rectangle({
                        strokeColor: '#00FF00',
                        strokeOpacity: 0.75,
                        strokeWeight: 1.5,
                        fillColor: '#00FF00',
                        fillOpacity: 0.25,
                        map: this.map,
                        bounds: {
                            north: 1,
                            south: -1,
                            east: 1,
                            west: -1
                        }
                    });

                    break;
            }

            this._super();
            // AbstractField.prototype.start.call(this);
        },

        _renderReadonly: function () {
            console.log('_renderReadonly');

            const options = this.attrs.options;
            const value = this._getValue();

            if (value === undefined) {
                return;
            }

            switch (options.mode) {
                case 'marker':
                    this.map.setCenter(value.position);
                    this.map.setZoom(value.zoom);

                    this.marker.draggable = false;
                    this.marker.setPosition(value.position);

                    this.marker.setMap(this.map);
                    break;

                case 'rectangle':
                    this.rectangle.setBounds(value.rectangle);

                    this.rectangle.setMap(this.map);
                    break;
            }

            const thisMap = this.map;
            setTimeout(function () {
                google.maps.event.trigger(thisMap, 'resize');
            }, 500);
        },

        _renderEdit: function () {
            console.log('_renderEdit');

            let that = this;
            let options = this.attrs.options;

            this.map.addListener('zoom_changed', function () {
                let value = that._getValue();
                value.zoom = that.map.getZoom();
                that._setValue(value);
            });

            switch (options.mode) {
                case 'marker':
                    this.marker.draggable = true;
                    this.marker.addListener('drag', function (event) {
                        let value = that._getValue();
                        value.position = {
                            lat: event.latLng.lat(),
                            lng: event.latLng.lng()
                        };
                        that._setValue(value);
                    });
                    break;

                case 'rectangle':
                    this.rectangle.setBounds(value.rectangle);

                    this.rectangle.setMap(this.map);
                    break;
            }
        },

        _formatValue: function (value) {
            try {
                return JSON.stringify(value);
            } catch (e) {
                return '{}';
            }
        },

        _parseValue: function (value) {
            try {
                return JSON.parse(value);
            } catch (e) {
                return undefined;
            }
        },

        _getValue: function () {
            const value = this._parseValue(this.value);

            if (!value) {
                return {
                    position: {
                        lat: 0,
                        lng: 0
                    },
                    zoom: 0
                }
            }

            return value;
        },

        _setValue: function (value, options) {
            this.isDirty = true;
            this._doDebouncedAction();

            console.log(value);
            return this._super(value, options);
        }
    });

    registry.add('googlemaps', GoogleMaps);

    return {
        'GoogleMaps': GoogleMaps
    };
});
