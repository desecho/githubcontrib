function deleteRepo(id, element){
  $.ajax({
    type: 'POST',
    url: urlDeleteRepo,
    data: {id: id},
    success: function() {
      $(element).parent().remove()
    }
  })
}
