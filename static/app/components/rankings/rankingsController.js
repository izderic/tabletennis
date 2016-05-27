var rankingsController = angular.module('rankingsController', []);


rankingsController.controller('RankingsController', function ($scope, $routeParams, $http) {

    $scope.rankings = [];

    $http.get("/api/rankings/?league=" + $routeParams.id).success(function (data) {
        $scope.rankings = data;
    });
});