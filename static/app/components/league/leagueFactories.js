var leagueFactories = angular.module('leagueFactories', []);


leagueFactories.factory('League', function ($resource) {
    return $resource('/api/leagues/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });
});


leagueFactories.factory('Round', function ($resource) {
    return $resource('/api/rounds/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });
});
