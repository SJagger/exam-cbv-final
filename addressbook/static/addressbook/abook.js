$(document).ready(function() {
  var ShowForm = function() {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      // dataType: 'json',
      beforeSend: function() {
        $('#modal-book').modal('show');
      },
      success: function(data) {
        $('#modal-book .modal-content').html(data);
      }
    });
  };

  var SaveForm = function(){
    var form = $(this);
    $.ajax({
      url: form.attr("data-url"),
      data: form.serialize(),
      type: form.attr('method'),
      // dataType: 'json',
      success: function(data){
        if(data){
          $('#book-table tbody').html($(data).find('#tbody-tab').html());
          $('#modal-book').modal('hide');
        }
        else {
          $('#modal-book .modal-content').html(data);
        }
      }
    })
    return false;
  }

// Create
$('.js-create').click(ShowForm);
$('#modal-book').on('submit','.create-form',SaveForm);

// Update
$('#book-table').on('click','.js-update',ShowForm);
$('#modal-book').on('submit','.update-form',SaveForm);

// Delete
$('#book-table').on('click','.js-delete',ShowForm);
$('#modal-book').on('submit','.delete-form',SaveForm);

});
