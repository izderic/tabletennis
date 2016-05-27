var matchesController = angular.module('matchesController', []);


matchesController.controller('MatchesController', function ($scope, $routeParams, $http, Round) {
    $scope.rounds = Round.query({league: $routeParams.id});
});


matchesController.controller('MatchController', function ($scope, $http, $routeParams, $location, Match) {

    $scope.match = Match.get({id: $routeParams.id});
    $scope.success = false;
    $scope.loading = false;

    $scope.addSet = function (matchId) {
        $scope.match.sets.push({match: matchId});
    };

    $scope.removeSet = function (item) {
        var index = $scope.match.sets.indexOf(item);
        $scope.match.sets.splice(index, 1);
    };

    $scope.submit = function (match) {
        var id = match.id;

        $scope.match.$update(
            function () {
                $location.url('/match/' + id);
                $scope.success = true;
                $scope.loading = false;
            },
            function (error) {
                $scope.errors = error.data;
            });
    }

});
