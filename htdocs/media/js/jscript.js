$(document).ready
(
	function()
	{
		$("#accept_license").click
		(
	  		function()
			{
				if ($("#accept_license").is(":checked"))
				{
  					$('#start_setup').removeAttr("disabled");
				}
				else
				{
					$('#start_setup').attr("disabled","true");
				}
			}
		);				
	 }
);