$("p#userquestion").hide();
$("p#reflexion").hide();
$("p#answer").hide();

$("input#adress").click(function() {
	$("input#adress").focus();
});

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
        $("p#userquestion").show();
        $("p#userquestion").text("si j'ai bien compris, tu me demande de chercher «" + $("#question").val() + "».");
        $("p#reflexion").show();
        if (data.error === 1) {
            $("p#reflexion").text("Et bien je n'ai pas compris ta requète, essai de t'exprimer clairement");
        } else {
            $("form#champs").hide();
            function thinking() {
                charList = ["\/", "―", "\\", "|"]
                if (int < 30) {
                    $("p#reflexion").text("Laisse moi quelques secondes chercher ça " + charList[charUsed]);
                    charUsed += 1;
                    if (charUsed === 4) {
                        charUsed = 0;
                    }
                    int += 1
                } else {
                    $("p#reflexion").text("J'ai trouvé ça:");
                    $("p#answer").show();
                    $("p#answer").html("Histoire du lieu:" + "<br>" + data.summary);
                    var map = L.map('mapid').setView([data.lat, data.longi], 15);
                    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    maxZoom: 18,
                    id: 'mapbox.streets',
                    accessToken: 'pk.eyJ1Ijoic3NnbWFzdGVyIiwiYSI6ImNqeGF5dGFpajA2YmgzbnBud253ZmMwYm8ifQ.RFvKLrjywTTEEou9gRHG4A'
                    }).addTo(map);
                    var marker = L.marker([data.lat, data.longi]).addTo(map);
                    var geocodeService = L.esri.Geocoding.geocodeService();
                    geocodeService.reverse().latlng([data.lat, data.longi]).run(function(error, result) {
                        L.marker([data.lat, data.longi]).addTo(map).bindPopup(result.address.Match_addr).openPopup();
                    });
                    clearInterval(intervalId);
                }
            }
            var intervalId = setInterval(thinking, 250);
        }
    });

    event.preventDefault();

});
