// Notification JavaScripts

(function ($) {
	'use strict';

	$('.noty-selectize-config').selectize({
		create: false,
		sortField: {
			field: 'text',
			direction: 'asc'
		},
		dropdownParent: 'body'
	});

	var i = -1;
  	var msgs = ['You have successfully trigger notification', 'Second notification', 'I saw you hit 3 times!', 'Time to stop?', 'I said enough!'];

  	$('.show-noty').on('click', function () {
	    var msg = $('#noty-message').val(),
	        type = $('#noty-messenger-type').val().toLowerCase(),
	        position = $('#noty-position').val();
	    if (!msg) {
	        msg = getMessage();
	    }
	    if (!type) {
	        type = 'error';
	    }
	    noty({
	        theme: 'app-noty',
	        text: msg,
	        type: type,
	        timeout: 3000,
	        layout: position,
	        closeWith: ['button', 'click'],
	        animation: {
	        	open: 'noty-animation fadeIn',
	        	close: 'noty-animation fadeOut'
	        }
	    });
	});

	$('.show-error-noty').on('click', function () {

		var msg = 'Error Message',
	        type = 'error',
			position = 'topRight';
			

			noty({
				theme: 'app-noty',
				text: msg,
				type: type,
				timeout: 3000,
				layout: position,
				closeWith: ['button', 'click'],
				animation: {
					open: 'noty-animation fadeIn',
					close: 'noty-animation fadeOut'
				}
			});
	});

  function getMessage() {
      i++;
      if (i === msgs.length) {
          i = 0;
      }
      return msgs[i];
  }


})(jQuery);