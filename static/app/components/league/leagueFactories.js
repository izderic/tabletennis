var leagueFactories = angular.module('leagueFactories', []);


leagueFactories.factory('League', function ($resource) {
    var League = $resource('/api/leagues/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });

    return League;
});


leagueFactories.factory('Round', function ($resource) {
    var Round = $resource('/api/rounds/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });

    return Round;
});


leagueFactories.factory('Match', function ($resource) {
    var Match = $resource('/api/matches/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });

    return Match;
});