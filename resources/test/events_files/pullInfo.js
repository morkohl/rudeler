var oldcontent2;
var data2;
/* 
 * @author Robin Schuster
 * @date 27.7.2013
 */
//pullUserInfo();
setInterval(function(){ //SetInterval 8sec
   pullUserInfo(); 
},10000);

/**
 * 
 * @Description Starts the Script ajax_pullUserInfo.php and execute all Actions in the Script
 * 
 */
function pullUserInfo(){
    /*$.get("ajax_pullUserInfo.php",function(data){
    eval(data);
});*/

$.post("ajax_universal.php", {art: "titlebar_statussymbols"}, function(data) {
		if (oldcontent != data)
		{
			oldcontent = data;
      data = data.trim();
			// format and output result

			//$("#funksprueche").fadeOut("fast");
			$("#titlebar_statussymbols").html(
				data
			);
			//$("#funksprueche").fadeIn("fast");
		}
	}, "html");
  
  /*$.post("ajax_universal.php", {art: "sidebar_loggedin_nachrichten"}, function(data2) {
		if (oldcontent2 != data2)
		{
			oldcontent2 = data2;
			// format and output result

			//$("#funksprueche").fadeOut("fast");
			$("#NachrichtenCenter").style(
				data2
			);
			//$("#funksprueche").fadeIn("fast");
		}
	}, "html");*/

}

function setFriendInfo (count){
    if(count < 1 ){
        
    }else{
        
    }
}

function setGenerallyInfo (count){
    if(count < 1 ){
        
    }else{
        
    }
}


function setMessageInfo(count){

    var count_angezeigt = count;
    if(count < 1 ){
        $("#NachrichtenCenter").css("background-color","#F8F8F8");
        $("#NachrichtenCenter").find("a").css("color","#5E832B");
        //$("#NachrichtenCenter").find("img").remove();
        //$("#NachrichtenCenter_zahl").find("div").html("");
        /*var $NachrichtenTitleBar = $("#NachrichtenTitleBar").find("img"),
        isNull = $NachrichtenTitleBar.is(function(){
           // alert($NachrichtenTitleBar.attr("src"));
           return $NachrichtenTitleBar.attr("src") === "http://airsoft-verzeichnis.de/bilder/icons/nachrichten_leer_27.png";
        });
        /*alert(isNull);
        if(!isNull){
          $("#NachrichtenTitleBar").find("img").attr("src","http://airsoft-verzeichnis.de/bilder/icons/nachrichten_leer_27.png");  
        } 
        $("#NachrichtenTitleBar").find("div").remove();
        //alert($("#NachrichtenTitleBar").find("img").attr("src"));*/
    
    }else{
        if(count > 9) count_angezeigt = "+";
        $("#NachrichtenCenter").css("background-color","#5E832B");
        $("#NachrichtenCenter").find("a").css("color","#ffffff");
        //if(!($("#NachrichtenCenter").find("img").is("*"))){
             //$("#NachrichtenCenter").append("<img border=\"0\" style=\"margin-left:3px;\" src=\"http://airsoft-verzeichnis.de/nachricht_7.jpg\">");
        //}
        /*if(!( $("#NachrichtenTitleBar").find("div").is("*"))){
             $("#NachrichtenTitleBar").find("img").attr("src","http://airsoft-verzeichnis.de/bilder/icons/nachrichten_plus_27.png");
             $("#NachrichtenTitleBar").append("<div style=\"width:10px; height:11px; padding:0px; z-index:999; position:absolute; margin-left:87px; font-weight:bold; margin-top:-24px; background:#FF9900; color:#fff; font-size:9px; text-align:center; vertical-align:middle;\">"+count_angezeigt+"</div>");
        }
        else if($("#NachrichtenTitleBar").find("div").html() != count_angezeigt)
        {
            $("#NachrichtenTitleBar").find("div").html(count_angezeigt);  
        }
        
        //$("#NachrichtenCenter_zahl").find("div").html(count);*/
        
        
        
        
    }
}
 
function setThreadInfo (count){
    if(count < 1 ){
        
    }else{
        
    }
}
