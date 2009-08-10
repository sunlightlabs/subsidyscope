 function handleCarouselClick(tabToFadeIn)
    {   
	    var tabContainers = $('div.tabs > div');
    	tabContainers.each(function(i){						
	    	if($(this).css('display')!='none')
		    {
			    $(this).fadeOut(300, function(){									
				    tabToFadeIn.fadeIn(300);
    			});
	    	}
		    else
    		{
	    		$(this).hide();
		    }
    	});						

      $('div.tabs ul.tabNavigation a').removeClass('selected');
      $('div.tabs ul.tabNavigation a[href=#' + tabToFadeIn.attr('id') + ']').addClass('selected');
      return false;	
    }

$(function () {   
	// handle initial cookie index
	var SUBSIDYSCOPE_CAROUSEL_COOKIE_NAME = 'SubsidyscopeInitialCarouselIndex'+window.location.href;
	var carouselInterval = null;
	var initialTabToShowIndex = getCookie(SUBSIDYSCOPE_CAROUSEL_COOKIE_NAME);
	if (initialTabToShowIndex==null)
	{
		initialTabToShowIndex = 0;
	}
	else
	{
		initialTabToShowIndex = parseInt(initialTabToShowIndex);
	}
	setCookie(SUBSIDYSCOPE_CAROUSEL_COOKIE_NAME, ((initialTabToShowIndex+1) % $('div.tabs > div').length), 30);

	// handle initial tab display
	var tabContainers = $('div.tabs > div');
	tabContainers.hide().filter(':eq(' + initialTabToShowIndex + ')').show();                        

	// unhide the tab nav
	$('#feature_box .feature_circle img').css('display','inline');
		
	// establish handlers for clicking the tab nav
	$('div.tabs ul.tabNavigation a').click(function() {		        
		clearInterval(carouselInterval);
		handleCarouselClick($(this.hash));
		return false;
	});	
   
	// set up carousel auto-rotation
	carouselInterval = setInterval(function(){
		var buttonToClick = null;
		var selectedTabButton = $('div.tabs ul.tabNavigation a.selected');
		if (selectedTabButton.length==0)
			// if nothing has been clicked, the "selected" class won't be set
			selectedTabButton = $('div.tabs ul.tabNavigation a:eq(' + initialTabToShowIndex + ')');
		
		// if there's a selected button, click the next one
		buttonToClick = selectedTabButton.parent().next().find('a');
		// ...unless it was the last one, in which case click the first one
		if(buttonToClick.length==0)
				buttonToClick = $('div.tabs ul.tabNavigation a:first');

		if(buttonToClick.length>0)
			handleCarouselClick($(buttonToClick.attr('href')));
	}, 8000);
});
