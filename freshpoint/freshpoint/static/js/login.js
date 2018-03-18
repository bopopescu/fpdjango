 $("#login-button").click(function(event){
		 event.preventDefault();

	 $('form').fadeOut(500);
	 $('.wrapper').addClass('form-success');
	 //$(location).attr('href', '{% url "index" %}');
	 var url = $(this).data('target');
	 setTimeout(
            function() {
                location.replace(url);
            }, 1000);
	 });