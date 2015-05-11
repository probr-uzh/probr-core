'use strict';

angular.module('probrApp')
	.factory('Device', function (djResource) {
      var Device = djResource('/api/devices/:deviceId/', {deviceId:'@id'},
      {
          getStatus: {method: 'GET', url: '/api/devices/:deviceId/statuses/', isArray: true}
        }
      );
      return Device;
    });
