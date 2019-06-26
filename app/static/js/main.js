$("p#answer").hide();

$("input#adress").click(function() {
	$("input#adress").focus();
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
var int = 0;

function addElem(cleanAdress) {
    var adress = {
            adress: cleanAdress,
        }
    ajaxPost("lien vers serveur à ajouter", adress,
        function (reponse) {
        	$("p#answer").show();
        	var intervalId = setInterval(thinking, 500);
        }
    );
}


$("button#send").on('click', function(event) {
	$.ajax({
		data : {
			name : $('#nameInput').val(),
			email : $('#emailInput').val()
		},
		type : 'POST',
		url : '/process'
	})
	.done(function(data) {
		if (data.error) {
			$('#errorAlert').text(data.error).show();
			$('#successAlert').hide();
		}
		else {
			$('#successAlert').text(data.name).show();
			$('#errorAlert').hide();
		}

	});
	$("p#answer").show();
	var map = L.map('mapid').setView([48.858053, 2.294289], 15);
	function thinking() {
    	charList = ["\/", "―", "\\", "|"]
    	if (int < 15) {
        	$("p#answer").text("Laisse moi réfléchir " + charList[charUsed]);
        	charUsed += 1;
			if (charUsed === 4) {
				charUsed = 0;
			}
        	int += 1
    	} else {
        	clearInterval(intervalId);
    	}
	}
	var intervalId = setInterval(thinking, 500);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoic3NnbWFzdGVyIiwiYSI6ImNqeGF5dGFpajA2YmgzbnBud253ZmMwYm8ifQ.RFvKLrjywTTEEou9gRHG4A'
	}).addTo(map);
	event.preventDefault();
});
