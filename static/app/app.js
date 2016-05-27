var app = angular.module('LeagueApp', [
    'ngRoute', 'ngResource', 'homeController', 'playerController', 'playerFactories', 'leagueController', 'leagueFactories', 'matchesController',
    'matchDirectives', 'rankingsController', 'matchesFactories', 'rankingsFactories'
]);

app.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            controller: 'HomeController',
            templateUrl: '/static/app/components/home/views/home.html'
        })
        .when('/players', {
            controller: 'PlayerListController',
            templateUrl: '/static/app/components/player/views/player_list.html'
        })
        .when('/player/create', {
            controller: 'PlayerCreateController',
            templateUrl: '/static/app/components/player/views/player_create.html'
        })
        .when('/player/update/:id', {
            controller: 'PlayerEditController',
            templateUrl: '/static/app/components/player/views/player_edit.html'
        })
        .when('/player/delete/:id', {
            controller: 'PlayerDeleteController',
            templateUrl: '/static/app/components/player/views/player_confirm_delete.html'
        })
        .when('/leagues', {
            controller: 'LeagueListController',
            templateUrl: '/static/app/components/league/views/league_list.html'
        })
        .when('/league/create', {
            controller: 'LeagueCreateController',
            templateUrl: '/static/app/components/league/views/league_create.html'
        })
        .when('/league/update/:id', {
            controller: 'LeagueEditController',
            templateUrl: '/static/app/components/league/views/league_edit.html'
        })
        .when('/league/delete/:id', {
            controller: 'LeagueDeleteController',
            templateUrl: '/static/app/components/league/views/league_confirm_delete.html'
        })
        .when('/matches/:id', {
            controller: 'MatchesController',
            templateUrl: '/static/app/components/matches/views/matches.html'
        })
        .when('/match/:id', {
            controller: 'MatchController',
            templateUrl: '/static/app/components/matches/views/match.html'
        })
        .when('/rankings/:id', {
            controller: 'RankingsController',
            templateUrl: '/static/app/components/rankings/views/rankings.html'
        })
        .otherwise({
            redirectTo: '/'
        });
    $locationProvider.html5Mode(true);
});

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
