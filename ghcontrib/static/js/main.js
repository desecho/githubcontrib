'use strict';

$.jGrowl.defaults.closerTemplate = '<div>' + gettext('Close all notifications') + '</div>';

angular.module('app', ['ngResource', 'angular-loading-bar', 'ngCookies']);
angular.module('app').factory('appFactory', function() {
  return {
    displayMessage: function(message) {
      return $.jGrowl(message);
    },
  };
});
angular.module('app').directive('ngEnter', function() {
  return function(scope, element, attrs) {
    element.bind('keydown keypress', function(event) {
      if (event.which === 13) {
        scope.$apply(function() {
          scope.$eval(attrs.ngEnter);
        });
        event.preventDefault();
      }
    });
  };
});

(function() {
  angular.module('app').factory('appResourceInterceptor', appResourceInterceptor);
  appResourceInterceptor.$inject = ['$cookies'];

  function appResourceInterceptor($cookies) {
    return {
      request: function(config) {
        const headers = {
          'X-CSRFToken': $cookies.get('csrftoken'),
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest',
        };
        angular.extend(config.headers, headers);
        return config;
      },
    };
  }

  angular.module('app').config(config);
  config.$inject = ['$httpProvider', '$interpolateProvider', '$resourceProvider'];

  function config($httpProvider, $interpolateProvider, $resourceProvider) {
    $httpProvider.interceptors.push('appResourceInterceptor');
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
  }

  angular.module('app').controller('MenuController', MenuController);

  function MenuController() {
    let vm = this;
    vm.changeLanguage = changeLanguage;

    function changeLanguage() {
      angular.element('#language-form').submit();
    }
  }
})();

let vars = {}; // eslint-disable-line no-unused-vars
let urls = {}; // eslint-disable-line no-unused-vars

function createPostResource(name, url) { // eslint-disable-line no-unused-vars
  angular.module('app').factory(name, factory);
  factory.$inject = ['$resource'];

  function factory($resource) {
    return $resource(url, {}, {
      post: {
        method: 'POST',
      },
    });
  }
}
