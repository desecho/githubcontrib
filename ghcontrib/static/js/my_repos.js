'use strict';

(function() {
  createPostResource('DeleteRepo', urls.urlDeleteRepo);
  createPostResource('AddRepo', urls.urlAddRepo);
  createPostResource('LoadCommitData', urls.urlLoadCommitData);
  angular.module('app').controller('MyReposController', MyReposController);
  MyReposController.$inject = ['DeleteRepo', 'AddRepo', 'LoadCommitData', 'appFactory'];

  function MyReposController(DeleteRepo, AddRepo, LoadCommitData, appFactory) {
    const vm = this;
    vm.deleteRepo = function($event) {
      const element = $event.target;
      const id = angular.element(element).data('id');
      DeleteRepo.post(angular.element.param({
        id: id,
      }), function(response) {
        vm.repos = vm.repos.filter(function(repo) {
          if (response.status === 'success') {
            if (repo.id != id) {
              return id;
            }
          } else {
            appFactory.displayMessage(response.error);
          }
        });
      }, function() {
        appFactory.displayMessage(gettext('Error deleting repository'));
      });
    };

    vm.addRepo = function() {
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
    };

    vm.loadCommitData = function() {
      LoadCommitData.post(angular.element.param({
        name: vm.name,
      }), function(response) {
        if (response.status !== 'success') {
          appFactory.displayMessage(response.error);
        }
      }, function() {
        appFactory.displayMessage(gettext('Error loading commit data'));
      });
    };

    vm.loadRepos = function() {
      vm.repos = vars.repos;
      angular.element('#repos').show();
    };
  }
})();
