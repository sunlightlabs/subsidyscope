var BAILOUT_fields = {'ftd': 'Funding to Date', 'pff': 'Potential Future Funding', 'sc': 'Subsidy Cost'};

function BAILOUT_format_breakdown(sum, f, max_value)
{
	if(sum==null)
		return '';
	
	var inner = [];
	var classes_outer = [f];
	
	if(sum.is_null || sum.is_unknown)
		inner.push('<div class="bar bar-unknown">unknown</div>');
	
	if(sum.is_na)
	{
	    inner.push('<div class="n-a">N/A</div>');
	}
	
	// just a straight-up dollar amount
	if((sum.value!=null)&&(!sum.is_unlimited))
	{
		var width = Math.floor( 100.0 * Math.abs(sum.value) / max_value) + '%';
		inner.push('<div class="bar bar-normal bar-solid" style="width:' + width + '"><span class="value-amount">$' + sum.value + 'b</span></div>');
	}
	
	// value is unlimited and no part of it is known
	if((sum.is_unlimited)&&(sum.value==null))
	{
		inner.push('<div class="bar bar-unlimited">unlimited</div>');
	}
	
	// the 'at least $xxxb' case...
	if((sum.is_unlimited)&&(sum.value!=null))
	{
	    var width = Math.floor( 100.0 * Math.abs(sum.value) / max_value) + '%';
		inner.push('<div class="bar bar-normal bar-solid" style="width:' + width + '"></div>');
		inner.push('<div class="bar bar-unlimited">at least $' + sum.value + 'b</div>');
	}	    
		
	if(sum.value!=null && !sum.is_unlimited && (sum.value<750))
	{
		classes_outer.push('trailing-label');
		classes_outer.push('trailing-label-' + Math.floor(Math.abs(sum.value)/50.0));
	}
	
	return '<div class="bar-container ' + classes_outer.join(' ') + '">' + inner.join('') + '<div class="clear"></div></div>';
}

var last_agency = null;

function BAILOUT_init(p_target_node, p_agency)
{   
	var max_value = 0;

	var json_data = {% include "bailout/bailout_programs.json" %};
	
	var computed_data = new Object();
	var agency_i = 0;
	for(agency in json_data)
	{	    
		computed_data[agency] = new Object();			
		
		for(f in BAILOUT_fields)
		{
			computed_data[agency][f] = new Object();
			computed_data[agency][f].is_null = false;
			computed_data[agency][f].is_unknown = false;
			computed_data[agency][f].is_unlimited = false;
			computed_data[agency][f].is_na = false;
			computed_data[agency][f].value = null;
		}
		
		for(program in json_data[agency])
		{	
			computed_data[agency][program] = new Object();
							
			for(f in BAILOUT_fields)
			{
				computed_data[agency][program][f] = new Object();
				computed_data[agency][program][f].is_null = false;
				computed_data[agency][program][f].is_unknown = false;
				computed_data[agency][program][f].is_unlimited = false;
				computed_data[agency][program][f].is_na = false;
				computed_data[agency][program][f].value = null;								
				
				var v = json_data[agency][program][f];
				if(v==null)
				{
					computed_data[agency][f].is_null = true;
					computed_data[agency][program][f].is_null = true;
				}
				else if(v=='unknown')
				{
					computed_data[agency][f].is_unknown = true;
					computed_data[agency][program][f].is_unknown = true;
				}
				// is amount unlimited or in the form e.g. '500+' ?
				else if((v=='unlimited')|| ((typeof(v)=='string') && v.match(/\d+\+/) ))
				{
					computed_data[agency][f].is_unlimited = true;
					computed_data[agency][program][f].is_unlimited = true;
					
					if(v.match(/\d+\+/))
					{
					    v = v.replace('+','');
					    computed_data[agency][f].value += parseInt(v);	
    					computed_data[agency][program][f].value += parseInt(v);
					}
				}
				else if(v=='n.a.')
				{
				    computed_data[agency][f].is_na = true;
					computed_data[agency][program][f].is_na = true;
				}
				else
				{
					if(computed_data[agency][f].value==null)
						computed_data[agency][f].value = 0;
					if(computed_data[agency][program][f].value==null)
						computed_data[agency][program][f].value = 0;
					
					computed_data[agency][f].value += parseInt(v);	
					computed_data[agency][program][f].value += parseInt(v);					
				}
			}
		}
		
		for(f in BAILOUT_fields)
			max_value = Math.max(max_value, computed_data[agency][f].value);
	}
	
	// separate loop is necessary so that we can get the max bar size before drawing any
	for(agency in json_data)
	{
	    if((p_agency!=null)&&(p_agency!=agency))
	        continue;
	    
		// create the agency container		
		var breakdown = '';
		/*
		for(f in BAILOUT_fields)
			breakdown += BAILOUT_format_breakdown(computed_data[agency][f], f, max_value);
		breakdown = '<div class="breakdown">' + breakdown + '</div>';
		*/
			
		var subtitle = ((json_data[agency]._subtitle!=null) && (json_data[agency]._subtitle!=agency)) ? '<div class="full-name">' + json_data[agency]._subtitle + '</div>' : '';			

		var tooltip = '';
		//var tooltip = '<div class="agency-tooltip" id="agency-tooltip-' + agency_i + '"><h4 class="tooltip-title">' + tooltip + '</h4></div>';
			
		var agency_div = $('<div id="agency-' + agency_i + '" class="agency">' + tooltip + '<div class="left-block"><a class="agency-title" id="agency-title-' + agency_i + '" href="#agency-' + agency_i + '">' + agency + '</a>' + subtitle + '</div><div class="programs"></div><div class="clear"></div></div>');			
	
		// append the programs to it
		var program_i = 0;
		var programs = [];
		for (program in json_data[agency])
		{
			if(program.substring(0,1)=='_')
				continue;
				
			var breakdown = '';
			for(f in BAILOUT_fields)
				breakdown += BAILOUT_format_breakdown(computed_data[agency][program][f], f, max_value);
				
			var program_description = '';
			if(json_data[agency][program].desc!=null)
				program_description = '<div class="program-description">' + json_data[agency][program].desc + '</div>';
			
			var program_div = $('<div id="program-' + agency_i + '-' + program_i + '" class="program"><div class="left-block"><div class="program-name">' + program + '</div>' + program_description + '<div style="clear:right"></div></div><div class="breakdown">' + breakdown + '</div><div class="clear"></div></div>');
			agency_div.find('.programs').append(program_div);				
			program_i++;
		}
		
		agency_div.find('.left-block').hover(
			function(){
				$(this).find('.program-description').fadeIn();
			},
			function(){
				$(this).find('.program-description').fadeOut();
			}
		);															
	
		// add the agency
		$(p_target_node).append(agency_div);
	
		last_agency = agency_div;
	
		agency_i++;
	}

}

function DrawBailoutVisualizationLegend(target_node, p_to_date, p_future)
{
    var to_date = 'Disbursements';
    var future = 'Potential Disbursements';
    if(p_to_date!=null) { to_date = p_to_date; }
    if(p_future!=null) { future = p_future; }
    $(target_node).html('<div id="legend"><div class="legend-item ftd"><div class="legend-square">&nbsp;</div>' + to_date + '</div><div class="legend-item pff"><div class="legend-square">&nbsp;</div>' + future + '</div><div class="legend-item sc"><div class="legend-square">&nbsp;</div>Estimated Subsidy</div></div><div class="clear"></div>');
}

function DrawBailoutVisualization(target_node, agency)
{
	$(document).pngFix(); // IE transparency fix
	BAILOUT_init(target_node, agency);    
}