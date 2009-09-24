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
    
    // make slide-toggle-able fieldsets
    $('fieldset#advanced-options legend').click(function(){
       $(this).parent().toggleClass('collapsed'); 
    });
        
    // hook up program radio buttons
    $('#program-selector ul li label input').click(function(){
        DisplayProgramPanel($('#program-selector ul li input:checked').val());
    });    

    // hook up datepicker
    $('#obligation-date-wrapper input[type=text]').datepicker();

    // tabs-ify results section
    $('#tabs').tabs();
		
	$('#tabs').bind('tabsselect', function(event, ui) {

		if(ui.index == 1)
		{
			window.location.href = window.location.href.replace(/\#.*$/,'') + '#faads-result-graph';		
			loadChartFlash();			
		}			
		else if(ui.index == 2)
		{
			window.location.href = window.location.href.replace(/\#.*$/,'') + '#faads-result-map';		
			loadMapFlash();
		}	
		else if(ui.index==3)
		{
			window.location.href = window.location.href.replace(/\#.*$/,'') + '#faads-result-summary';				
		    loadSummary();
		}
	
	});
	
    // load supplemental objects as necessary
    if(window.location.href.indexOf('#faads-result-map')!=-1)
    {
        loadMapFlash();
        window.location.hash = 'faads-result-map';        
    }
    if(window.location.href.indexOf('#faads-result-summary')!=-1)
    {
        loadSummary();
        window.location.hash = 'faads-result-summary';       
    }
    if(window.location.href.indexOf('#faads-result-graph')!=-1)
    {        
        loadChartFlash();
        window.location.hash = 'faads-result-graph';        
    }


    $("select[name='dataType']").change(
	function()
	{
		if ($("select[name='dataType']").val() == 'state')
		{	
			setDataField(1);
			setLabelText('Total Spending (2000-2009)');
		}
		else if ($("select[name='dataType']").val() == 'state_per_capital')
		{
			setDataField(3);
			setLabelText('Per Capita Spending (2000-2009)');
		}
	});
	
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