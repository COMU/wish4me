function checkEnter(e){
  var check=((e.keyCode || 0) !== 13);
  if (!check) {
    //lets post the city name to gather the locations around
      $.ajax({
          type: "POST",
          data: $('#searchTextField').serialize(),
          url: "/wish/locations",
          cache: false,
          dataType: "html",
          success: function(html, textStatus) {
            console.log("ok");
          },
          error: function (XMLHttpRequest, textStatus, errorThrown) {
              console.log(XMLHttpRequest);
              //$('#locations').replaceWith('No place detected around');
          }
      });

    return false;
  }
}

