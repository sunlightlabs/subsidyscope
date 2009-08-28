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
    
    // wrap checkbox label contents
    $('#program-selection-program ul li label').each(function(i){
        var parts = $(this).html().split('>');
        var checkbox = parts.shift();
        var rest = parts.join('>');
       $(this).html(checkbox + '> <span class="program-title">' + rest.replace(/^\s+/,'') + '</span>'); 
    });
    
    
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
    $('fieldset legend').click(function(){
       $(this).parent().toggleClass('collapsed'); 
    });
    
    // $('select[multiple]').multiSelect(  
    // {  
    //     select_all_min: 3,  
    //     no_selection: "No criteria selected",  
    //     selected_text: " selected"  
    // });

    // hook up tags dropdown to CFDA
    $('#id_tags').change(function(){
      var cfda_program_numbers = $(this).val().split(',');
      var label = $(this).get(0).options[$(this).get(0).selectedIndex].text;
      $('#cfda-programs input[type=checkbox]').attr('checked', false);
      for(var i=0; i<cfda_program_numbers.length; i++)
      {
        var program_number = cfda_program_numbers[i];
        $('#cfda-programs input[value=' + program_number + ']').attr('checked',true);
      }
      $(this).val('');
      $('#multiSelect-id_cfda_programs-title').text('All ' + label + ' Programs');
    });
    
    // display active program selection dialog
    $('#program-selection-' + $('#program-selector ul li input:checked').val()).slideDown();
    
    // hook up program radio buttons
    $('#program-selector ul li input').change(function(){
        DisplayProgramPanel($('#program-selector ul li input:checked').val());
    });
    
    // rename multiselect title -- necessary?
    $('#multiSelect-id_cfda_programs-title').text('Select specific CFDA programs')

    // hook up datepicker
    $('#obligation-date-wrapper input[type=text]').datepicker();

    // tabs-ify results section
    $('#tabs').tabs();

    $("select[name='dataType']").change(
	function()
	{
		if ($("select[name='dataType']").val() == 'state')
		{	
			setDataField(1);
		}
		else if ($("select[name='dataType']").val() == 'state_per_capital')
		{
			setDataField(3);
		}
	});
	
});



	
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