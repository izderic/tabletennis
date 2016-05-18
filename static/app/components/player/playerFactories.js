var playerFactories = angular.module('playerFactories', []);

playerFactories.factory('Player', function ($resource) {
    var Player = $resource('/api/players/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });

    return Player;
});
