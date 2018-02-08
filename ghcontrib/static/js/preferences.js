app.factory('SavePreferences', ['$resource', function($resource) {
  return $resource(urlSavePreferences, {}, {
    post: {
      method: 'POST',
      headers: headers
    },
  });
}]);

app.controller('PreferencesController', ['$scope', 'SavePreferences',
  function($scope, SavePreferences) {
    $scope.savePreferences = function(reload) {
      const preferences = {
        language: $('input:radio[name=lang]:checked').val()
      };
      SavePreferences.post($.param(preferences), function() {
        if (reload) {
          location.reload();
        }
      }, function() {
        displayMessage(gettext('Error saving settings'));
      });
    };
  }
]);
