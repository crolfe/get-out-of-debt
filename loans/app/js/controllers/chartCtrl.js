'use strict';

loans.controller('ChartCtrl', ['$scope', '$q', '$log', '$window', 'APIService', function ($scope, $q, $log, $window, APIService) {

  var host;
  if ($window.location.origin.indexOf('http://127.0.0.1') > -1 || $window.location.origin.indexOf('http://localhost') > -1) {
    host = 'http://127.0.0.1:8000';  // TODO either set this to prod URL, or set it in app.config somewhere
  } else {
    host = $window.location.origin;  // use actual hostname when in staging or production
  }
  $scope.debtRows = [
    {"debt_name": "", "principal": 0, "monthly_payment": 0, "extra_payment": 0, "interest_rate": 0}
  ];
  $scope.addDebtRow = function () {
    $scope.debtRows.push({"debt_name": "", "principal": 0, "monthly_payment": 0, "extra_payment": 0, "interest_rate": 0});
  };
  $scope.removeDebtRow = function (index) {
    $scope.debtRows.splice(index, 1);
    if ($scope.debtRows.length === 0) {
      $scope.addDebtRow();  // allow the old row to be cleared, but we still need to show one in the view
    }
  };
  $scope.closeAlert = function (parentIndex, index, key) {
    $scope.errors[parentIndex][key].splice(index, 1);  // some of the keys can be a list instead of single string
    if ($scope.errors[parentIndex][key].length === 0) {
      delete $scope.errors[parentIndex][key];  // no sense keeping the empty list
    }
  };
  $scope.calculate = function () {
    var paymentsPromise = APIService.post(host + '/api/loans/calculate', $scope.debtRows);
    $q.all([paymentsPromise]).then(function (resultsArray) {
      $log.info('got some datas!');
      $scope.chartData = resultsArray[0];
      $scope.debtFree = resultsArray[0].labels[resultsArray[0].labels.length - 1];
      $scope.scaleStepWidth = $scope.chartData.scaleStepWidth;
      /* add the chart to an iterable so we can dynamically add it to DOM using ng-repeat, which is super hacky,
            but need this issue to be resolved: https://github.com/petermelias/angular-chartjs/issues/11
      */
      $scope.charts = [{
        scaleOverlay : false,
        scaleOverride : true,
        scaleSteps : 20,
        scaleStepWidth : $scope.chartData.scaleStepWidth,
        scaleStartValue : 0,
        scaleLineColor : "rgba(0,0,0,.1)",
        scaleLineWidth : 1,
        scaleShowLabels : true,
        scaleLabel : "<%=value%>",
        scaleFontFamily : "'HelveticaNeue-Light','Helvetica Neue','proxima-nova'",
        scaleFontSize : 12,
        scaleFontStyle : "normal",
        scaleFontColor : "#909090",
        scaleShowGridLines : true,
        scaleGridLineColor : "rgba(0,0,0,.05)",
        scaleGridLineWidth : 1,
        bezierCurve : false,
        pointDot : true,
        pointDotRadius : 3,
        pointDotStrokeWidth : 1,
        datasetStroke : true,
        datasetStrokeWidth : 2,
        datasetFill : true,
        animation : true,
        animationSteps : 60,
        animationEasing : "easeOutQuart",
        onAnimationComplete : null
      }];
    }, function (error) {
      $scope.errors = error.data;
    });
  };
}]);
