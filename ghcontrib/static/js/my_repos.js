app.factory('DeleteRepo', ['$resource', function($resource) {
  return $resource(urlDeleteRepo, {}, {
    post: {method: 'POST', headers: headers}
  });
}]);

app.factory('AddRepo', ['$resource', function($resource) {
  return $resource(urlAddRepo, {}, {
    post: {method: 'POST', headers: headers}
  });
}]);

app.factory('LoadCommitData', ['$resource', function($resource) {
  return $resource(urlLoadCommitData, {}, {
    post: {method: 'POST', headers: headers}
  });
}]);

app.controller('MyReposController', ['$scope', 'DeleteRepo', 'AddRepo', 'LoadCommitData',
function ($scope, DeleteRepo, AddRepo, LoadCommitData) {
  $scope.deleteRepo = function($event){
    const element = $event.target;
    const id = $(element).data('id')
    DeleteRepo.post($.param({id: id}), function(){
      $scope.repos = $scope.repos.filter(function(repo){
        if (repo.id != id) {
          return id;
        }
      });
    }, function(){
      displayMessage(gettext('Error deleting repository'));
    });
  };
  $scope.addRepo = function(){
    AddRepo.post($.param({name: $scope.name}), function(response){
      if (response.status === 'success') {
        $scope.repos.push({id: response.id, name: $scope.name})
        $scope.name = '';
      } else {
        displayMessage(response.error);
      }
    }, function(){
      displayMessage(gettext('Error adding repository'));
    });
  };
  $scope.loadCommitData = function(){
    LoadCommitData.post($.param({name: $scope.name}), function(response){
      if (response.status !== 'success') {
        displayMessage(response.error);
      }
    }, function(){
      displayMessage(gettext('Error loading commit data'));
    });
  };
}]);

function loadRepos(){
  var scope = angular.element($('#my-repos-controller')).scope();
  scope.$apply(function(){
    scope.repos = repos;
  });
  $('#repos').show();
}

$(function(){
  loadRepos();
});
