var matchesController = angular.module('matchesController', []);


matchesController.controller('MatchesController', function ($scope, $routeParams, $http) {

    $scope.rounds = [];

    $http.get("/league/matches/" + $routeParams.id + "/").success(function (data) {
        $scope.rounds = data;
    });
});

matchesController.controller('MatchController', function ($scope, $http, $routeParams) {

    $scope.match = {};

    $http.get("/league/match/" + $routeParams.id + "/").success(function (data) {
        $scope.match = data;
    });

    $scope.addSet = function () {
        $scope.match.sets.push({});
    };

    $scope.removeSet = function (item) {
        var index = $scope.match.sets.indexOf(item);
        $scope.match.sets.splice(index, 1);
    };

    $scope.submit = function (match) {
        var id = match.id;
        $http.post("/league/match/" + $routeParams.id + "/", match).success(function (data, status) {


        })
    }


});