'use strict';

(function() {
  angular.module('app').factory('repo', factory);
  factory.$inject = ['$resource'];

  function factory($resource) {
    return $resource(urls.urlRepo + ':id/', {
      id: '@id',
    }, {
      add: {
        method: 'POST',
      },
      delete: {
        method: 'DELETE',
      },
    });
  }
})();

(function() {
  angular.module('app').factory('commitData', factory);
  factory.$inject = ['$resource'];

  function factory($resource) {
    return $resource(urls.urlLoadCommitData, {}, {
      load: {
        method: 'POST',
      },
    });
  }
})();

(function() {
  angular.module('app').controller('MyReposController', MyReposController);
  MyReposController.$inject = ['repo', 'commitData', 'appFactory'];

  function MyReposController(repo, commitData, appFactory) {
    const vm = this;
    vm.deleteRepo = deleteRepo;
    vm.addRepo = addRepo;
    vm.loadCommitData = loadCommitData;
    vm.repos = vars.repos;

    function deleteRepo(repoId) {
      repo.delete({
        id: repoId,
      }, function(response) {
        if (response.status === 'success') {
          vm.repos = vm.repos.filter(function(repo) {
            if (repo.id != repoId) {
              return repo;
            }
          });
        } else {
          appFactory.displayMessage(response.error);
        }
      }, function() {
        appFactory.displayMessage(gettext('Error deleting repository'));
      });
    }

    function addRepo() {
      repo.add(angular.element.param({
        name: vm.name,
      }), function(response) {
        if (response.status === 'success') {
          vm.repos.push({
            id: response.id,
            name: vm.name,
          });
          vm.name = '';
        } else {
          appFactory.displayMessage(response.error);
        }
      }, function() {
        appFactory.displayMessage(gettext('Error adding repository'));
      });
    }

    function loadCommitData() {
      commitData.load({}, function(response) {
        if (response.status !== 'success') {
          appFactory.displayMessage(response.error);
        }
      }, function() {
        appFactory.displayMessage(gettext('Error loading commit data'));
      });
    }
  }
})();
