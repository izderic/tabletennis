var rankingsController = angular.module('rankingsController', []);


rankingsController.controller('RankingsController', function ($scope, $routeParams, Ranking, League) {

    $scope.rankings = Ranking.query({league: $routeParams.id});
    $scope.league = League.get({id: $routeParams.id});

    $scope.getClass = function getClass(index) {
        return {
            first: index == 0,
            second: index == 1,
            third: index == 2
        };
    };

});