'use strict';


loans.factory('APIService', ['$http', function ($http) {
    var promise, APIService;
    APIService = {
        get: function (url) {
            promise = $http.get(url).then(function (response) {
                return response.data;
            });
            return promise;
        },
        post: function (url, data) {
            promise = $http.post(url, data).then(function (response) {
                return response.data;
            });
            return promise;
        }
    };
    return APIService;
}]);