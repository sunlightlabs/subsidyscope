{% load media %}

var TARP_highlighted_rows = new Array();
var TARP_hidden_rows = new Array();

function TARP_hide_graph()
{
	$('#raphael-container').slideUp(800, function(){
		$('#tarp-table-container').animate({ height: 500 }, 800);
	});
}

function TARP_init()
{    
    // add SWF
    // junk parameter to force reload of flash data in IE
    var queryparam = new Date().getTime();
    
    /* initial tarp viz */
	
	
	swfobject.embedSWF('{% media_url %}/scripts/tarp-1.1.swf', 'tarpVis', '660', {{ visualization_settings.height }}, '9.0.0', '{% media_url %}/scripts/playerProductInstall.swf', {
       	       width: '660',
       	       height: {{ visualization_settings.height }},
       	       bar_width: {{ visualization_settings.bar_width }},
       	       bar_margin: {{ visualization_settings.bar_margin }},	       
       	       data_url: 'http://' + window.location.host + '{% url bailout.views.tarp_xml %}?' + queryparam,
       	       bar_color_0: '{{ visualization_settings.bar_color_1 }}',
       	       bar_color_1: '{{ visualization_settings.bar_color_2 }}',
       	       policy_file: 'http://' + window.location.host + '/crossdomain.xml'
       	   });
	
	
	/* end initial tarp viz */
	
	
	/* bubbles viz */
	
	
	swfobject.embedSWF('{% media_url %}/scripts/tarp-bubbles.swf', 'tarpBubbleVis', 700, 650, '9.0.0', '{% media_url %}/scripts/playerProductInstall.swf');
	
	/* end bubbles viz */
	
	
	/* by date viz */
	
	swfobject.embedSWF('{% media_url %}/scripts/TARPVis.swf', 'tarpTimelineVis', 620, 300, '9.0.0', '{% media_url %}/scripts/playerProductInstall.swf');
	
	/* end by-date viz */


	$('#tabs').tabs();

    $('#tarp-data-table tr').hover(
		function(){
			var transaction_id = this.id.replace(/row\-/,'');
			if(!($(this).find('.transaction-type').text().match(/dividend payment/i)))
			    TARP_highlight_graph_rect(transaction_id);
			TARP_highlight_table_row(transaction_id);
		},
		function(){		
		}
	);

    
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
                sorter:'dates' 
            },
            2: {
                sorter:'money'
            },
            4: {
                sorter:'money'
            }
        },
        sortList: [[0,0]],
        headerTable: $('#tarp-header-table').get(0)
    }); 
 
 
	$('#tarpFilterInput').autocomplete('/bailout/tarp/filter/institution/', {
		width: 260,
		selectFirst: false});
	
	function findValueCallback(event, data, formatted) {
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
		else
		{	
			$('#tarp-data-table tr').each(function(index)
			{
				$(this).removeClass('hidden')
			});
		}
	}
	
	
	$("#tarpFilterInput").result(findValueCallback).change(function() {
		$(this).search();
	});
	
	$("#tarpFilterInput").blur(function() {
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
	
	
	
	// do initial scrollto (horizontal doesn't work right for TARP container otherwise)
	$('#tarp-table-container').stop().scrollTo('0px', 50);
}

function getFlexMovie(movieName) {
    if (navigator.appName.indexOf("Microsoft") != -1) {
        return window[movieName]
    }
    else {
        return document[movieName]
    }
}


function TARP_highlight_graph_rect(id)
{
	var flex = null;
	flex = getFlexMovie("tarp");
	if((flex!=null) && (flex.flexHighlightBar!=null))
	    flex.flexHighlightBar(id);	
	   
	var flexTimeline = null;
	flexTimeline = getFlexMovie("tarpTimelineVis"); 
	if((flexTimeline!=null) && (flexTimeline.selectNodeByTransactionId!=null))
		flexTimeline.selectNodeByTransactionId(id);

}

function TARP_highlight_table_row(id, scroll)
{
    if(scroll==null)
        scroll = false;
    
	// scrolling & highlighting in table
	while(n = TARP_highlighted_rows.pop())
		$(n).removeClass('highlighted');
	var row_id = '#row-' + id;
	$(row_id).addClass('highlighted');
	TARP_highlighted_rows.push(row_id);
	
	if(scroll)
	    $('#tarp-table-container').stop().scrollTo(row_id, 800);
}


$(document).ready(function(){
	TARP_init();
});
