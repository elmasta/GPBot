$("div#answer").hide();
$("button#restart").hide();
$("p#middlebar").hide();
$("input#adress").focus();

var charUsed = 0;
var int = 0;

$("button#send").on("click", function(event) {

	$.ajax({
		data : {
			question : $("#question").val()
		},
		type : "POST",
		url : "/process"
	})
	.done(function(data) {
        $("form#champs").hide();
        $("div#answer").show();
        function thinking() {
            charList = ["\/", "―", "\\", "|"]
            if (int < 30) {
                $("p#gpbot").html("Si j'ai bien compris, tu me demande de chercher «" + data.question + "». <br> Laisse moi quelques secondes chercher ça . . . " + charList[charUsed]);
                charUsed += 1;
                if (charUsed === 4) {
                    charUsed = 0;
                }
                int += 1
            } else {
                if (data.error === 1) {
                    $("p#gpbot").text("Et bien je n'ai pas compris ta requète, essai de t'exprimer clairement");
                } else {
                    if (data.summary === ". . . Hum il n'y a rien dans mon encyclopédie, étrange. . .") {
                        $("p#gpbot").html("Tu m'avais demandé «" + data.question + "». <br>" + data.quote + "<br>" + data.summary);
                    } else {
                        $("p#middlebar").show();
                        $("p#gpbot").html("Tu m'avais demandé «" + data.question + "». <br>" + data.quote);
                        $("p#result").text(data.summary);
                    }
                    var map = L.map("mapid").setView([data.lat, data.longi], 15);
                    L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    maxZoom: 18,
                    id: "mapbox.streets",
                    accessToken: "pk.eyJ1Ijoic3NnbWFzdGVyIiwiYSI6ImNqeGF5dGFpajA2YmgzbnBud253ZmMwYm8ifQ.RFvKLrjywTTEEou9gRHG4A"
                    }).addTo(map);
                    L.marker([data.lat, data.longi]).addTo(map).bindPopup(data.formatted_adress).openPopup();
                    clearInterval(intervalId);
                }
                $("button#restart").show();
            }
        }
        var intervalId = setInterval(thinking, 250);
    });
    event.preventDefault();
});
