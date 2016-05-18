var playerController = angular.module('playerController', []);


playerController.controller('PlayerListController', function ($scope, Player) {
    $scope.players = Player.query();
});

playerController.controller('PlayerCreateController', function ($scope, Player, $location) {

        $scope.player = new Player({});
        $scope.errors = {};

        $scope.save = function () {
            $scope.player.$create(function () {
                $location.url('/players');
            },
            function (error) {
                $scope.errors = error.data;
            });

        };
    });

playerController.controller('PlayerEditController', function ($scope, Player, $location, $routeParams) {

        $scope.player = Player.get({id: $routeParams.id});
        $scope.errors = {};

        $scope.save = function () {
            $scope.player.$update(function () {
                $location.url('/players');
            },
            function (error) {
                $scope.errors = error.data;
            });

        };
    });

playerController.controller('PlayerDeleteController', function ($scope, Player, $location, $routeParams) {

        $scope.player = Player.get({id: $routeParams.id});

        $scope.remove = function () {
            $scope.player.$delete(function () {
                $location.url('/players');
            });

        };
    });