'use strict';

var loans = angular
  .module('loanApp', [
    'tc.chartjs',
    'ui.router',
    'mm.foundation'
  ]).config(['$urlRouterProvider', '$stateProvider', function ($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
      .state('home', {
        url: '/',
        controller: 'ChartCtrl',
        templateUrl: '/static/views/main.html'
      });
  }]);
