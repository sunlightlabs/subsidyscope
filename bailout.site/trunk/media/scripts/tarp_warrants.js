
function TARP_init()
{  
	var lastSearch;
	
	// add parser through the tablesorter addParser method 
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'dates', 
        is: function(s) { 
            // return false so this parser is not auto detected 
            return false; 
        }, 
        format: function(s) { 
            // format your data for normalization 
            var m = s.match(/<!\-\-\sordinal:\s(\d+)\s\-\->/);
            if(m==null)
                return s;
            else
                return m[1];
        }, 
        // set type, either numeric or text 
        type: 'numeric' 
    }); 
    
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'money', 
        is: function(s) { 
            // return false so this parser is not auto detected 
            return false; 
        }, 
        format: function(s) { 
            // format your data for normalization 
            if(s.toLowerCase()=='not confirmed')
                return -1;
            else
                return s.replace(/[^\d]/g,''); 
        }, 
        // set type, either numeric or text 
        type: 'numeric' 
    });
        
    $("#tarp-data-table").tablesorter({ 
        headers: { 
            0: { 
                sorter:'isoDate' 
            },
            2: {
                sorter:'currency'
            },
            4: {
                sorter:'currency'
            },
            5: {
                sorter:'currency'
            },
            6: {
                sorter:'percent'
            }
        },
        sortList: [[0,0]],
        headerTable: $('#tarp-header-table').get(0)
    }); 
    
    $('#tarpFilterInput').autocomplete('/projects/bailout/tarp/filter/institution/', {
		width: 260,
		selectFirst: false});
	
	function findValueCallback(event, data, formatted) {
		if (data)
		{
			lastSearch = $('#tarpFilterInput').val();
			
			if(this != false)
			{
				var show = {}
				
				var ids = data[1].split(',');
				
				jQuery.each(ids, function(){
					show['row-' + this] = true;
				});  
				
				$('#tarp-data-table tr').each(function(index)
				{
					var row_id = this.id;
					if(show[row_id])
						$(this).removeClass('hidden')
					else
						$(this).addClass('hidden')
				});
				
			}
			else
			{	
				$('#tarp-data-table tr').each(function(index)
				{
					$(this).removeClass('hidden')
				});
			}
		
		}
		else
		{	
			$('#tarp-data-table tr').each(function(index)
			{
				$(this).removeClass('hidden')
			});
		}
	}
	
	
	$("#tarpFilterInput").result(findValueCallback).change(function() {
		if($("#tarpFilterInput").val() != lastSearch)
			$(this).search();
	});
	
	$("#tarpFilterInput").blur(function() {
		if($("#tarpFilterInput").val() != lastSearch)
			$(this).search();
	});
	
	$("#tarpFilterInput").result(function(event, data, formatted) {
		if (data)
		{
			if(this != false)
			{
				var show = {}
				
				var ids = data[1].split(',');
				
				
				jQuery.each(ids, function(){
				
					show['row-' + this] = true;
				});  
				
				$('#tarp-data-table tr').each(function(index)
				{
					var row_id = this.id;
					if(show[row_id])
						$(this).removeClass('hidden')
					else
						$(this).addClass('hidden')
				});
				
			}
			else
			{	
				$('#tarp-data-table tr').each(function(index)
				{
					$(this).removeClass('hidden')
				});
			}
		
		}

	});
}

$(document).ready(function(){
	TARP_init();
}); 