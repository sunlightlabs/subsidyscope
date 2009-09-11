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
			swfobject.embedSWF("/media/scripts/open-flash-chart.swf?v=2", "resultsgraph", "880", "400", "9.0.0", "expressInstall.swf", {'data-file': '/projects/transportation/direct-expenditures/search/by-year/', 'data-query':'{{ query|safe }}'});
			
		else if(ui.index == 2)
			swfobject.embedSWF('{% media_url %}/scripts/SpendingMap.swf?v=8', 'mapVis', 800, 650, '9.0.0', '{% media_url %}/scripts/playerProductInstall.swf', {'mapPath':'/media/data/', 'dataPath':'/projects/transportation/direct-expenditures/search/map/','dataQuery':'{{ query|safe }}'}, {wmode:'transparent'});
	
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