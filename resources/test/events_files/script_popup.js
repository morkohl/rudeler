var t;
var oldcontent;
function get_popup_content(art_input, var1_input, var2_input, var3_input)
{
	$.post("ajax_popup.php", {art: art_input, var1: var1_input, var2: var2_input, var3: var3_input}, function(data) {
		if (oldcontent != data)
		{
			oldcontent = data;
      data = data.trim();
			// format and output result

			$("#popupwindow").html(
				data
			);
		}
	}, "html");
}