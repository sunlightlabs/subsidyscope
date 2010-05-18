var last_selected_program_panel = null;

function DisplayProgramPanel(panel)
{
    if(last_selected_program_panel==null)
        $('.program-selection-target').hide();
    else
        $('#program-selection-' + last_selected_program_panel).hide();
    $('#program-selection-' + panel).show();
    last_selected_program_panel = panel;    

}

$(document).ready(function(){    
    
    $('#obligation_date').removeClass('header headerAsc headerDesc');
    $('#cfda_program').removeClass('header headerAsc headerDesc');
    $('#recipient').removeClass('header headerAsc headerDesc');
    $('#amount').removeClass('header headerAsc headerDesc');
    
    // hacky...
    if (sortColumn=='vendor_name'){
        sortColumn = 'recipient';
    }
    
  	var columns = ['obligation_date', 'recipient', 'amount'];

    for (i in columns) {
        var thisColumn = columns[i];
            
        $('#' + thisColumn).removeClass('header headerAsc headerDesc');
    
        if(sortColumn==thisColumn) {
            $('#' + thisColumn).addClass('header' + (sortOrder=='asc' ? 'Asc': 'Desc'));
            $('#' + thisColumn).attr('rel', (thisColumn + ';' + (sortOrder=='asc' ? 'desc' : 'asc')));
        }
        else {
            $('#' + thisColumn).addClass('header');
            $('#' + thisColumn).attr('rel', (thisColumn + ';desc'));
        }
        
        $('#' + thisColumn).bind('click', function(e){            
            $('#sortField').val($(this).attr('rel').split(';')[0]);
            $('#sortOrder').val($(this).attr('rel').split(';')[1]);
			$('#sortForm').submit();
        });        
    }
    
    
    // display the initially-selected "choose programs by" div
    DisplayProgramPanel($('#program-selector ul li input:checked').val());
    
    // set up "select all"/"select none" links
    $('.select-all-or-none a.select-all').click(function(){
       $(this).parent().parent().find('ul li input[type=checkbox]').attr('checked', true); 
       return false;
    });    
    $('.select-all-or-none a.select-none').click(function(){
       $(this).parent().parent().find('ul li input[type=checkbox]').attr('checked', false); 
       return false;
    });
    
    
    if($('fieldset#advanced-options').hasClass('collapsed'))
 	   $('#search-options-state').text('[show]');
    else
 	   $('#search-options-state').text('[hide]');
    
    // make slide-toggle-able fieldsets
    $('fieldset#advanced-options legend').click(function(){
       $(this).parent().toggleClass('collapsed'); 
       
       if($(this).parent().hasClass('collapsed'))
    	   $('#search-options-state').text('[show]');
       else
    	   $('#search-options-state').text('[hide]');
       
    });
    
        
    // hook up program radio buttons
    $('#program-selector ul li label input').click(function(){
        DisplayProgramPanel($('#program-selector ul li input:checked').val());
    });    

    // hook up datepicker
    $('#obligation-date-wrapper input[type=text]').datepicker({ defaultDate: -365, minDate: new Date("January 1, 2000"), maxDate: new Date() });

    // tabs-ify results section
    $('#tabs').tabs();
		
	$('#tabs').bind('tabsselect', function(event, ui) {

		if(ui.index == 1)
		{
			window.location.href = window.location.href.replace(/\#.*$/,'') + '#fpds-result-graph';		
			loadChartFlash();			
		}			
		else if(ui.index == 2)
		{
			window.location.href = window.location.href.replace(/\#.*$/,'') + '#fpds-result-map';		
			loadMapFlash();
		}	
		else if(ui.index==3)
		{
			window.location.href = window.location.href.replace(/\#.*$/,'') + '#fpds-result-summary';				
		    loadSummary();
		}
	
	});
	
    // load supplemental objects as necessary
    if(window.location.href.indexOf('#fpds-result-map')!=-1)
    {
        loadMapFlash();
        window.location.hash = 'fpds-result-map';        
    }
    if(window.location.href.indexOf('#fpds-result-summary')!=-1)
    {
        loadSummary();
        window.location.hash = 'fpds-result-summary';       
    }
    if(window.location.href.indexOf('#fpds-result-graph')!=-1)
    {        
        loadChartFlash();
        window.location.hash = 'fpds-result-graph';        
    }


    $("select[name='dataType']").change(
	function()
	{
		if ($("select[name='dataType']").val() == 'state')
		{	
			setDataField(1);
			setLabelText('Total Spending');
		}
		else if ($("select[name='dataType']").val() == 'state_per_capital')
		{
			setDataField(3);
			setLabelText('Per Capita Spending');
		}
	});
	
	$("select[name='dataType']").val('state');
	setDataField(1);
	setLabelText('Total Spending');

	
});



function setLabelText(labelText)
{
	var flex = null;
	flex = getFlexMovie("mapVis");
	if((flex!=null) && (flex.setLabelText!=null))
	    flex.setLabelText(labelText);	
}
	
	
function setDataField(fieldId)
{
	var flex = null;
	flex = getFlexMovie("mapVis");
	if((flex!=null) && (flex.setDataField!=null))
	    flex.setDataField(fieldId);	
}
	
function getFlexMovie(movieName) 
{
    if (navigator.appName.indexOf("Microsoft") != -1) 
    {
        return window[movieName]
    }
    else 
    {
        return document[movieName]
	}
}