$(document).ready(function() {
  var ShowForm = function() {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
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
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      success: function(data){
        var tabb = $("#tbody-tab");
        if(form.attr("class")=="create-form"){
          data.success
          alert(data.message);
          var row = "<tr id='data-" + data.pk + "'>\
                          <td>" + data.fname + "</td>\
                          <td>" + data.lname + "</td>\
                          <td>" + data.cnumber + "</td>\
                          <td>" + data.address + "</td>\
                          <td><button type='button' class='btn btn-info js-update' data-toggle='modal' data-target='#modal-book' data-url=" + data.update_url + ">\
                                Update</button>\
                              <button type='button' class='btn btn-danger js-delete' data-toggle='modal' data-target='#modal-book' data-url=" + data.delete_url + ">\
                                Delete</button>\
                          </td>\
                    </tr>";
          tabb.append(row);
          $("#modal-book").modal("hide");
        }
        else if(form.attr("class")=="update-form"){
          data.success
          alert(data.message);
          var edited = "<tr id='data-" + data.pk + "'>\
                          <td>" + data.fname + "</td>\
                          <td>" + data.lname + "</td>\
                          <td>" + data.cnumber + "</td>\
                          <td>" + data.address + "</td>\
                          <td><button type='button' class='btn btn-info js-update' data-toggle='modal' data-target='#modal-book' data-url=" + data.update_url + ">\
                                Update</button>\
                              <button type='button' class='btn btn-danger js-delete' data-toggle='modal' data-target='#modal-book' data-url=" + data.delete_url + ">\
                                Delete</button>\
                          </td>\
                    </tr>";
          $("#data-" + data.pk).replaceWith(edited);
          $("#modal-book").modal('hide');
        }
        else if(form.attr("class")=="delete-form"){
          data.success
          alert(data.message);
          $("#data-" + data.pk).remove();
          $("#modal-book").modal('hide');
        }
        else {
          $("#modal-book .modal-content").html(data);
        }
      }
    });
    return false;
  };

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
