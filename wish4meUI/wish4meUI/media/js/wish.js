function setDefaultPrivacy(send_id) {
  in_ajax = 1;
  send_address = '/wishlist/' + send_id+'/getPrivacy'
  $.post(send_address, function(data){
    if(data == "private")
      $('#id_ModelFormMetaclass-is_private').attr('checked', 'checked');
    if(data == "public")
      $('#id_ModelFormMetaclass-is_private').removeAttr('checked');
  }
  );
  in_ajax = 0;
}

function setAutoChangePrivacy() {
  $('#id_ModelFormMetaclass-related_list').change(function() {
    send_id = $('#id_ModelFormMetaclass-related_list option:selected').attr('value');
    if(send_id != "") {
      setDefaultPrivacy(send_id);
    }
  });
}
