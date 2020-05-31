$(document).ready(function(){

    //Blur Links (Prevents Outline)
    $('a').click(function() {
        this.blur();
    });

    //when a section is requested a section, hide all others and show it
    //also animate the detailbox in
    $('ul.dishlist > li > a').click(function() {
       var requestedSection = this.href.substring(this.href.indexOf('#'));
       //alert(requestedSection);
       if (requestedSection.length <= 1){
           throw 'error in link. anchor missing';
       }
       //we just show the requested. Unshown when the close button is clicked.
       $(requestedSection).show();
        //Call in the info box
       $("#fade_bg").fadeIn();
       $("#detailbox").animate({bottom: '0px' }, 1000);

       return false;
    });

//when the close button or the background is clicked, remove the detailbox and hide the text
    
    $('#fade_bg #detailbox').click(
        function(e){
            e.stopPropagation();
        }
    );
    
    $('#fade_bg, #closeButton').click(function(){
        $("#fade_bg").fadeOut();
        $("#detailbox").animate({bottom: '-1000px' }, 500, function() {
            //hide all visible sections
            $('#detailbox > div.detailboxcontent').hide()
        });
        return false;
    });

}); 
