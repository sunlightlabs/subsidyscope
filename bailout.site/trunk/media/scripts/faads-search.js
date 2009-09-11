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

$(function(){    
    
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
			loadChartFlash();
			
		else if(ui.index == 2)
			loadMapFlash();
	
	});
	

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