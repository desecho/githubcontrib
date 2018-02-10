'use strict';

(function() {
  angular.module('app').factory('preferences', factory);
  factory.$inject = ['$resource'];

  function factory($resource) {
    return $resource(urls.urlSavePreferences, {}, {
      save: {
        method: 'POST',
      },
    });
  }
})();

(function() {
  angular.module('app').controller('PreferencesController', PreferencesController);
  PreferencesController.$inject = ['preferences', 'appFactory'];

  function PreferencesController(preferences, appFactory) {
    let vm = this;
    vm.save = save;
    vm.language = vars.language;

    function save(reload) {
      preferences.save(angular.element.param(), function() {
        if (reload) {
          location.reload();
        }
      }, function() {
        appFactory.displayMessage(gettext('Error saving settings'));
      });
    }
  }
})();
