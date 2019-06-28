$("p#answer").hide();

$("input#adress").click(function() {
	$("input#adress").focus();
});

var charUsed = 0;
var int = 0;

$("button#send").on('click', function(event) {

	$.ajax({
		data : {
			question : $('#question').val()
		},
		type : 'POST',
		url : '/process'
	})
	.done(function(data) {
        //todo
		//if (data.error) {
		//	$('#errorAlert').text(data.error).show();
		//	$('#successAlert').hide();
		//}
        //else

        $("p#answer").show();
        var map = L.map('mapid').setView([data.lat, data.longi], 15);
        function thinking() {
            charList = ["\/", "―", "\\", "|"]
            if (int < 30) {
                $("p#answer").text("Laisse moi réfléchir " + charList[charUsed]);
                charUsed += 1;
                if (charUsed === 4) {
                    charUsed = 0;
                }
                int += 1
            } else {
                $("p#answer").text(data.summary);
                clearInterval(intervalId);
            }
        }
        var intervalId = setInterval(thinking, 250);
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1Ijoic3NnbWFzdGVyIiwiYSI6ImNqeGF5dGFpajA2YmgzbnBud253ZmMwYm8ifQ.RFvKLrjywTTEEou9gRHG4A'
        }).addTo(map);

    });

    event.preventDefault();

});
