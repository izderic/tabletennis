var matchesFactories = angular.module('matchesFactories', []);


matchesFactories.factory('Match', function ($resource) {
    return $resource('/api/matches/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });
});