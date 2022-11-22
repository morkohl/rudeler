var t;
var oldcontent;
function exec_function(art_input, var1_input, var2_input, var3_input)
{
	$.post("ajax_function.php", {art: art_input, var1: var1_input, var2: var2_input, var3: var3_input}, function(data) {

	}, "html");
}