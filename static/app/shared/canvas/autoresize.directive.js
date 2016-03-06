angular.module("flaederGamesApp")
    .directive("autoResize", ['$window', function ($window) {
        return {
            restrict: "A",
            scope: true,
            link: function (scope, element, attrs) {

                scope.ratio = parseInt(attrs.width) / parseInt(attrs.height);

                function resize() {
                    if (!document.fullscreenElement &&    // alternative standard method
                      !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {  // current working methods

                        var footer = angular.element(document).find('footer'),
                            header = angular.element(document).find('header'),
                            gameControlBar = document.getElementById('gameControlBar'),
                            hsize = $window.innerHeight - footer.prop('offsetHeight') - header.prop('offsetHeight') - gameControlBar.offsetHeight - 80,
                            wsize = hsize * scope.ratio;
                        element.css('height', hsize.toString() + 'px');
                        element.css('width', wsize.toString() + 'px');
                    }
                }

                $window.onresize = resize;
                resize();

            }
        };
    }]);
