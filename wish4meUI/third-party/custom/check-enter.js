$("#loading").hide();
$("#loading").ajaxStart(function(){
     $(this).show();
});

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

             //$.each(html, function(index, value) {

             //  list.push(value[1]);

             //});
             //$('#location').typeahead({
             //  source:list
             //});
            $('#location')
                .find('option')
                .remove()
                .end()
 
            $('#location')
                .append($("<option></option>")
                           .attr("value","")
                                    .text("")); 
             $.each(html, function(key, value) {   
                    $('#location')
                        .append($("<option></option>")
                                   .attr("value",value[0])
                                            .text(value[1])); 
             });
          
          $("#loading").hide();

          },
          error: function (XMLHttpRequest, textStatus, errorThrown) {
              console.log("error")
              console.log(XMLHttpRequest);
              //$('#locations').replaceWith('No place detected around');
          }
      });

    return false;
  }
  console.log("no entered");
}

