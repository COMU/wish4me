function bindPostCommentHandler() {
    $('#comment_form form').submit(function() {
        $.ajax({
            type: "POST",
            data: $('#comment_form form').serialize(),
            url: "/comments/post/",
            cache: false,
            dataType: "html",
            success: function(html, textStatus) {
                var result="<div class=\"alert alert-success\">" + html + "<\/div>";
                $('#comment_status').replaceWith(result).fadeOut('slow');
                bindPostCommentHandler();
                window.location.reload(true);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $('#comment_status').replaceWith('Your comment was unable to be posted at this time.  We apologise for the inconvenience.');
            }
        });
        return false;
    });
}
 
$(document).ready(function() {
    $('#navbarExample').scrollspy();
    bindPostCommentHandler();
});
