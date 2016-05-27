var leagueController = angular.module('leagueController', []);


leagueController.controller('LeagueListController', function ($scope, League) {
    $scope.leagues = League.query();
});

leagueController.controller('LeagueCreateController', function ($scope, League, Player, $location) {

        $scope.league = new League({
            num_of_sets: 2,
            points_per_set: 6
        });
        $scope.errors = {};
        $scope.availablePlayers = Player.query();

        $scope.save = function () {
            $scope.league.$create(function () {
                $location.url('/leagues');
            },
            function (error) {
                $scope.errors = error.data;
            });

        };
    });

leagueController.controller('LeagueEditController', function ($scope, League, Player, $location, $routeParams) {

        $scope.league = League.get({id: $routeParams.id});
        $scope.errors = {};
        $scope.availablePlayers = Player.query();

        $scope.save = function () {
            $scope.league.$update(function () {
                $location.url('/leagues');
            },
            function (error) {
                $scope.errors = error.data;
            });

        };
    });

leagueController.controller('LeagueDeleteController', function ($scope, League, $location, $routeParams) {

        $scope.league = League.get({id: $routeParams.id});

        $scope.remove = function () {
            $scope.league.$delete(function () {
                $location.url('/leagues');
            });

        };
    });
