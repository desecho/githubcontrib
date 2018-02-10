'use strict';

(function() {
  angular.module('app').factory('preferencesService', factory);
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
  angular.module('app').factory('preferencesDataservice', factory);
  factory.$inject = ['preferencesService', 'growl'];

  function factory(preferencesService, growl) {
    return {
      save: save,
    };

    function save(language) {
      return preferencesService.save(angular.element.param({
        language: language,
      }), function() {}, saveFail);

      function saveFail() {
        growl.error(gettext('Error saving settings'));
      }
    }
  }
})();

(function() {
  angular.module('app').controller('PreferencesController', PreferencesController);
  PreferencesController.$inject = ['preferencesDataservice'];

  function PreferencesController(preferencesDataservice) {
    let vm = this;
    vm.save = save;
    vm.language = vars.language;

    function save(reload) {
      preferencesDataservice.save(vm.language).$promise.then(function() {
        if (reload) {
          location.reload();
        }
      }).catch(function() {});
    }
  }
})();
