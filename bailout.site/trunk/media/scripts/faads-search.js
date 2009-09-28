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
    
  	if(sortColumn == 'obligation_date')
  	{
  		
  		if(sortOrder == 'asc')
  		{
  			$('#obligation_date').addClass('headerAsc');
  			
  			$('#obligation_date').bind('click', function(e){
  				$('#sortField').val('obligation_date');
  				$('#sortOrder').val('desc');
  				$('#sortForm').submit();
  			});
  		}	
  		else
  		{
  			$('#obligation_date').addClass('headerDesc');
  			
  			$('#obligation_date').bind('click', function(e){
  				$('#sortField').val('obligation_date');
  				$('#sortOrder').val('asc');
  				$('#sortForm').submit();
  			});
  		}
  			
  		$('#cfda_program').addClass('header');
    	$('#recipient').addClass('header');
    	$('#amount').addClass('header');
    	
    	
    	$('#cfda_program').bind('click', function(e){
			$('#sortField').val('cfda_program');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#recipient').bind('click', function(e){
			$('#sortField').val('recipient');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#amount').bind('click', function(e){
			$('#sortField').val('amount');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
    	
  	}
  	else if(sortColumn == 'cfda_program')
  	{
  		
  		if(sortOrder == 'asc')
  		{
  			$('#cfda_program').addClass('headerAsc');
  			
  			$('#cfda_program').bind('click', function(e){
  				$('#sortField').val('cfda_program');
  				$('#sortOrder').val('desc');
  				$('#sortForm').submit();
  			});
  		}
  		else
  		{
  			$('#cfda_program').addClass('headerDesc');
  			
  			$('#cfda_program').bind('click', function(e){
  				$('#sortField').val('cfda_program');
  				$('#sortOrder').val('asc');
  				$('#sortForm').submit();
  			});
  		}
  			
  		$('#obligation_date').addClass('header');
    	$('#recipient').addClass('header');
    	$('#amount').addClass('header');
    	
    	
    	$('#obligation_date').bind('click', function(e){
			$('#sortField').val('obligation_date');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#recipient').bind('click', function(e){
			$('#sortField').val('recipient');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#amount').bind('click', function(e){
			$('#sortField').val('amount');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
    	
  	}
  	else if(sortColumn == 'recipient')
  	{
  		if(sortOrder == 'asc')
  		{
  			$('#recipient').addClass('headerAsc');
  			
  			$('#recipient').bind('click', function(e){
  				$('#sortField').val('recipient');
  				$('#sortOrder').val('desc');
  				$('#sortForm').submit();
  			});
  		}
  		else
  		{
  			$('#recipient').addClass('headerDesc');
  		
  			$('#recipient').bind('click', function(e){
  				$('#sortField').val('recipient');
  				$('#sortOrder').val('asc');
  				$('#sortForm').submit();
  			});	
  		}
  			
  		$('#cfda_program').addClass('header');
 		$('#obligation_date').addClass('header'); 
    	$('#amount').addClass('header');
    	
    	
    	$('#cfda_program').bind('click', function(e){
			$('#sortField').val('cfda_program');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#obligation_date').bind('click', function(e){
			$('#sortField').val('obligation_date');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#amount').bind('click', function(e){
			$('#sortField').val('amount');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
    	
  	}
  	else if(sortColumn == 'amount')
  	{
  		if(sortOrder == 'asc')
  		{
  			$('#amount').addClass('headerAsc');

			$('#amount').bind('click', function(e){
  				$('#sortField').val('amount');
  				$('#sortOrder').val('desc');
  				$('#sortForm').submit();
  			});  			
  		}
  		else
  		{
  			$('#amount').addClass('headerDesc');
  			
  			$('#amount').bind('click', function(e){
  				$('#sortField').val('amount');
  				$('#sortOrder').val('asc');
  				$('#sortForm').submit();
  			});  	
  		}
  			
  		$('#cfda_program').addClass('header');
    	$('#recipient').addClass('header');
    	$('#obligation_date').addClass('header');
    	
    	
    	$('#cfda_program').bind('click', function(e){
			$('#sortField').val('cfda_program');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#recipient').bind('click', function(e){
			$('#sortField').val('recipient');
			$('#sortOrder').val('desc');
			$('#sortForm').submit();
		});
  			
  			
  		$('#obligation_date').bind('click', function(e){
			$('#sortField').val('obligation_date');
			$('#sortOrder').val('desc');
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
			
		else if(ui.index==3)
		    loadSummary();
	
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