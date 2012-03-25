function checkEnter(e){
  var check=((e.keyCode || 0) !== 13);
  if (!check) {
    //lets post the city name to gather the locations around
      $.ajax({
          type: "POST",
          data: $('#searchTextField').serialize(),
          url: "/wish/locations",
          cache: false,
          dataType: "json",
          success: function(html, textStatus) {
            var list = new Array();

             $.each(html, function(index, value) {

               list.push('"'+value+'"')

             });
             var new_value = "[" + new String(list) + "]";
             $('#location').attr('data-source', new_value);
          },
          error: function (XMLHttpRequest, textStatus, errorThrown) {
              console.log("error")
              console.log(XMLHttpRequest);
              //$('#locations').replaceWith('No place detected around');
          }
      });

    return false;
  }
}

