'use strict';

angular.module('app', ['ngResource', 'angular-loading-bar', 'ngCookies', 'angular-growl']);

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
  config.$inject = ['$httpProvider', '$interpolateProvider', '$resourceProvider', 'growlProvider'];

  function config($httpProvider, $interpolateProvider, $resourceProvider, growlProvider) {
    $httpProvider.interceptors.push('appResourceInterceptor');
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;

    growlProvider.globalTimeToLive(2000);
    growlProvider.globalDisableCountDown(true);
    growlProvider.globalDisableIcons(true);
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
