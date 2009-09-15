
(function($){
    $(document).ready(function(){
        $("#results").click( function(e) {
            var that = $(e.target);
            if( that.parents("li").hasClass("name")){
                if(that.is("a")) { that = that.parents("li");}
                var port = $(that).attr("name");   
                
                if(that.hasClass("close")){
                    that.removeClass("close");
                    that.removeClass("bold");
                    $(that).parent("ul").siblings("div.data-container").slideUp("normal", function(){$(this).remove();});
                    return false;
                }
                port = port.replace(/[+]/, "%2B");
                $.ajax({
                    'data': "code="+port,
                    'dataType': 'html',
                    'url': '/projects/transportation/aip/detail',
                    'success': function(html){
                        $(that).closest("div.portdetail").append(html).find("div.data-container").slideDown("fast");
                        $(that).addClass("close");
                        $(that).addClass("bold");
                    },
                    'error': function(xhr, textstatus){
                    }
                });
                return false;
            } else { return false; }
        });
    });    
})(jQuery);
