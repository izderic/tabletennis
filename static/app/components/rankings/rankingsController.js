var rankingsController = angular.module('rankingsController', []);


rankingsController.controller('RankingsController', function ($scope, $routeParams, Ranking, League) {
    $scope.rankings = Ranking.query({league: $routeParams.id});
    $scope.league = League.get({id: $routeParams.id});
});
