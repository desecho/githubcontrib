'use strict';

(function() {
  createPostResource('SavePreferences', urls.urlSavePreferences);
  angular.module('app').controller('PreferencesController', PreferencesController);
  PreferencesController.$inject = ['SavePreferences', 'appFactory'];

  function PreferencesController(SavePreferences, appFactory) {
    let vm = this;
    vm.savePreferences = function(reload) {
      const preferences = {
        language: angular.element('input:radio[name=lang]:checked')[0].value,
      };
      SavePreferences.post(angular.element.param(preferences), function() {
        if (reload) {
          location.reload();
        }
      }, function() {
        appFactory.displayMessage(gettext('Error saving settings'));
      });
    };
  }
})();
