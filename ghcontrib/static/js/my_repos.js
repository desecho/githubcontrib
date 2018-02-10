'use strict';

createPostResource('DeleteRepo', urls.urlDeleteRepo);
createPostResource('AddRepo', urls.urlAddRepo);

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
  MyReposController.$inject = ['DeleteRepo', 'AddRepo', 'commitData', 'appFactory'];

  function MyReposController(DeleteRepo, AddRepo, commitData, appFactory) {
    const vm = this;
    vm.deleteRepo = deleteRepo;
    vm.addRepo = addRepo;
    vm.loadCommitData = loadCommitData;
    vm.loadRepos = loadRepos;

    function deleteRepo(repo) {
      const id = repo.id;
      DeleteRepo.post(angular.element.param({
        id: repo.id,
      }), function(response) {
        if (response.status === 'success') {
          vm.repos = vm.repos.filter(function(repo) {
            if (repo.id != id) {
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
      AddRepo.post(angular.element.param({
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

    function loadRepos() {
      vm.repos = vars.repos;
      angular.element('#repos').show();
    }
  }
})();
