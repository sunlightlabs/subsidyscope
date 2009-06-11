$(function(){
    var page_url = location.href.replace(/http:\/\/[^\/]+/i,'');
    $('.section-floating-nav ul li a').removeClass('active').each(function(i){
        if($(this).attr('href')==page_url)
            $(this).addClass('active');
    });
})