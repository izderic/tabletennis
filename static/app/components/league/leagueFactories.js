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
