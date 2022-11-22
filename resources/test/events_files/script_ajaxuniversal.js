var t;
var oldcontent;
function get_universal_content(content_id_input, art_input, var1_input, var2_input, var3_input, var4_input, var5_input, var6_input, var7_input, var8_input, var9_input, var10_input, var11_input, var12_input, var13_input, var14_input)
{
	$.post("ajax_universal.php", {art: art_input, var1: var1_input, var2: var2_input, var3: var3_input, var4: var4_input, var5: var5_input, var6: var6_input, var7: var7_input, var8: var8_input, var9: var9_input, var10: var10_input, var11: var11_input, var12: var12_input, var13: var13_input, var14: var14_input, content_id: content_id_input}, function(data) {
		if (oldcontent != data)
		{
			oldcontent = data;
      data = data.trim();
			// format and output result

			$(content_id_input).html(
				data
			);
		}
	}, "html");
}