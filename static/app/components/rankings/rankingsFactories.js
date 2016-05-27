var rankingsFactories = angular.module('rankingsFactories', []);


rankingsFactories.factory('Ranking', function ($resource) {
    return $resource('/api/rankings/:id', { id: '@id' }, {
        'create': {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        },
        'update': { method: 'PUT' }
    });
});
