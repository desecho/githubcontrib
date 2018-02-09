'use strict';

(function() {
  createPostResource('savePreferences', urls.urlSavePreferences);
  angular.module('app').controller('PreferencesController', PreferencesController);
  PreferencesController.$inject = ['savePreferences', 'appFactory'];

  function PreferencesController(savePreferences, appFactory) {
    let vm = this;
    vm.save = save;
    vm.language = vars.language;

    function save(reload) {
      const preferences = {
        language: vm.language,
      };
      savePreferences.post(angular.element.param(preferences), function() {
        if (reload) {
          location.reload();
        }
      }, function() {
        appFactory.displayMessage(gettext('Error saving settings'));
      });
    }
  }
})();
