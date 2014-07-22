'use strict';

var loans = angular
  .module('loanApp', [
    'ui.router',
    'mm.foundation',
    'chartjs'
  ]).config(['$urlRouterProvider', '$stateProvider', function ($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
      .state('home', {
        url: '/',
        controller: 'ChartCtrl',
        templateUrl: '/static/loans/views/main.html'
      });
  }]);
