'use strict';

(function() {
  angular.module('app').factory('repoService', factory);
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
  angular.module('app').factory('repoDataservice', factory);
  factory.$inject = ['repoService', 'appFactory'];

  function factory(repoService, appFactory) {
    return {
      deleteRepo: deleteRepo,
      addRepo: addRepo,
    };

    function deleteRepo(repoId) {
      return repoService.delete({
        id: repoId,
      }, deleteRepoSuccess, deleteRepoFail);

      function deleteRepoSuccess(response) {
        if (response.status !== 'success') {
          appFactory.displayMessage(response.error);
        }
      }

      function deleteRepoFail() {
        appFactory.displayMessage(gettext('Error deleting repository'));
      }
    }

    function addRepo(name) {
      return repoService.add(angular.element.param({
        name: name,
      }), addRepoSuccess, addRepoFail);

      function addRepoSuccess(response) {
        if (response.status === 'success') {
          response.repo = {
            id: response.id,
            name: name,
          };
        } else {
          appFactory.displayMessage(response.error);
        }
      }

      function addRepoFail() {
        appFactory.displayMessage(gettext('Error adding repository'));
      }
    }
  }
})();


(function() {
  angular.module('app').factory('commitDataService', factory);
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
  angular.module('app').factory('commitDataDataservice', factory);
  factory.$inject = ['commitDataService', 'appFactory'];

  function factory(commitDataService, appFactory) {
    return {
      loadCommitData: loadCommitData,
    };

    function loadCommitData() {
      return commitDataService.load({}, loadCommitDataSuccess, loadCommitDataFail);

      function loadCommitDataSuccess(response) {
        if (response.status !== 'success') {
          appFactory.displayMessage(response.error);
        }
      }

      function loadCommitDataFail() {
        appFactory.displayMessage(gettext('Error loading commit data'));
      }
    }
  }
})();

(function() {
  angular.module('app').controller('MyReposController', MyReposController);
  MyReposController.$inject = ['commitDataDataservice', 'repoDataservice'];

  function MyReposController(commitDataDataservice, repoDataservice) {
    const vm = this;
    vm.addRepo = addRepo;
    vm.deleteRepo = deleteRepo;
    vm.loadCommitData = loadCommitData;
    vm.repos = vars.repos;

    function addRepo() {
      repoDataservice.addRepo(vm.name).$promise.then(
        function(response) {
          vm.repos.push(response.repo);
          vm.name = '';
        }
      ).catch(function() {});
    }


    function deleteRepo(repoId) {
      repoDataservice.deleteRepo(repoId).$promise.then(
        function() {
          vm.repos = vm.repos.filter(function(repo) {
            if (repo.id != repoId) {
              return repo;
            }
          });
        }
      ).catch(function() {});
    }

    function loadCommitData() {
      commitDataDataservice.loadCommitData();
    }
  }
})();
