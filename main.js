$("p#answer").hide();

$("input#adress").click(function() {
	$("input#adress").focus();
});

$("input#town").click(function() {
	$("input#town").focus();
});

function ajaxPost(url, data, callback, isJson) {
    var req = new XMLHttpRequest();
    req.open("POST", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Erreur réseau avec l'URL " + url);
    });
    if (isJson) {
    	req.setRequestHeader("Content-Type", "application/json");
    	data = JSON.stringify(data);
    }
    req.send(data);
}

var charUsed = 0;
var compteur = 0;

function addElem(cleanAdress) {
    var adress = {
            adress: cleanAdress,
            town: form.elements.town.value,
        }
    ajaxPost("lien vers serveur à ajouter", adress,
        function (reponse) {
        	$("p#answer").show();
        	var intervalId = setInterval(thinking, 500);
        }
    );
}

function thinking() {
    charList = ["\/", "―", "\\", "|"]
    if (compteur < 15) {
        $("p#answer").text("Laisse moi réfléchir " + charList[charUsed]);
        charUsed += 1;
		if (charUsed === 4) {
			charUsed = 0;
		}
        compteur += 1
    } else {
        clearInterval(intervalId);
    }
}

//parti test
//$("p#answer").show();

//$("button#send").on('click', function(event) {
//	$("p#answer").html = "coucou";
//});