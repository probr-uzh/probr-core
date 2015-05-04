'use strict';

angular.module('probrApp')
	.factory('Device', function (djResource) {
      var Device = djResource('/api/devices/:deviceId/', {deviceId:'@id'});
      return Device;
    });
