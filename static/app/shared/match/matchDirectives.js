var matchDirectives = angular.module('matchDirectives', []);


matchDirectives.directive('homeScore', function () {
    var link = function (scope, elm, attr, ngModel) {
        if (!ngModel) return;

        attr.$observe('ngModel', function (value) {
            ngModel.$validate();
        });

        scope.$watch('homeScore', function (homeScore) {
            ngModel.$validate();
        });

        ngModel.$validators.homeScore = function (awayScore) {
            var pointsPerSet = scope.match.league_round.league.points_per_set;
            var homeScore = scope.homeScore;

            return validateSet(homeScore, awayScore, pointsPerSet) && validateSet(awayScore, homeScore, pointsPerSet);
        };

        var validateSet = function (scoreOne, scoreTwo, pointsPerSet) {
            if (scoreOne == pointsPerSet)
                return scoreTwo - scoreOne == 2 || scoreOne - scoreTwo > 1;
            else if (scoreOne == pointsPerSet - 1)
                return scoreTwo - scoreOne == 2;
            else if (scoreOne < pointsPerSet - 1)
                return scoreTwo == pointsPerSet;
            else
                return Math.abs(scoreOne - scoreTwo) == 2;
        }
    };
    return {
        restrict: 'A',
        require: 'ngModel',
        scope: {
            homeScore: '=',
            match: '='
        },
        link: link
    };
});
