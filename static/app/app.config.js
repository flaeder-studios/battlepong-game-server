(function () {
    'use strict';

    angular.module('flaederGamesApp', ['ngRoute', 'ui.grid', 'ui.grid.saveState', 'ui.grid.selection', 'ngTable'])
        .constant('CONFIG', {
            test: 'jello'
        });
})();
