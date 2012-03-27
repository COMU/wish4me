function setPrivacy(wishlist_id, send_address) {
  in_ajax = 1;
  $.post(send_address, function(data){
    if(data == "private")
      $('#privacy-button-'+wishlist_id).button('toggle');
    if(data == "public")
      $('#privacy-button-'+wishlist_id).button('reset');
  }
  );
  in_ajax = 0;
} 
