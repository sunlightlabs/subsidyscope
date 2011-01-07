var rcsfield_head = new Array();
$(document).ready(function(){
    $('a.rcsfield-revision').each(function(i){
        rcsfield_head[$(this).attr('rel')] = $('#'+$(this).attr('rel')).val();
    });
        
    $('a.rcsfield-revision').click(function(){
        var morsel_field_id = $(this).attr('rel');
        if($(this).attr('href')=='#HEAD')
        {
            $('#' + morsel_field_id).val(rcsfield_head[morsel_field_id]);
        }
        else
        {
            $.get($(this).attr('href'), {}, function(data, status){
                $('#'+morsel_field_id).val(data);
            });
        }
        return false;
    });
});