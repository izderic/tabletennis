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
    };

    $scope.isValid = function(match) {
        var home = 0;
        var away = 0;
        var sets = match.sets;

        if (!sets)
            return true;

        var numOfSets = match.league_round.league.num_of_sets;

        for (var i=0; i<sets.length; i++) {
            var homePlayerScore = sets[i].home_player_score;
            var awayPlayerScore = sets[i].away_player_score;

            if (homePlayerScore > awayPlayerScore)
                home += 1;
            else
                away += 1;
        }

        return home == numOfSets && away < numOfSets || home < numOfSets && away == numOfSets || home < numOfSets && away < numOfSets;
    };

});
