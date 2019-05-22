$(document).ready(function() {
	$('.sidenav').sidenav();
	$('select').formSelect();
	$('#math').fadeOut(0);
	$('#slovene').fadeOut(0);
	$('#unsetModal').modal();
	$('#errorModal').modal();
});

function fadeIn(subject) {
	if (subject == "slovenscina") {
		$('#math').fadeOut(200);
		setTimeout(function() {
			$('#slovene').fadeIn(200);
		}, 210);
	} else {
		$('#slovene').fadeOut(200);
		setTimeout(function() {
			$('#math').fadeIn(200);
		}, 210);
	}
}

function makeRequest() {
	var params = [$('#predmet').val(),$('#raven').val(),$('#leto').val(),$('#rok').val()];

	if (params[0] == "unset") {
		$('#unsetModal').modal('open');
	} else {

		if (params[3] == "unset") {
			if (params[2] == "unset") {
				if (params[1] == "unset") {
					var addUrl = "/api?subject="+params[0];
				} else {
					var addUrl = "/api?subject="+params[0]+"&level="+params[1];
				}
			} else {
				var addUrl = "/api?subject="+params[0]+"&level="+params[1]+"&year="+params[2];
			}
		} else {
			var addUrl = "/api?subject="+params[0]+"&level="+params[1]+"&year="+params[2]+"&term="+params[3];
		}

		var requestUrl = addUrl;

		$.getJSON(requestUrl, function(data) {
			setImageAndUrl("data.Dodatno", "data.Path", "data.Rešitve");
			fadeIn(params[0]);
		}).fail(function() {
			$('#errorModal').modal('open');
		});

	}
}

function setImageAndUrl(addPath, exPath, url) {
	$('#dodatno').attr("src",addPath);
	$('#naloga').attr("src", exPath);
	$('#resitve').attr("href", url);
}

$('#show').click(function() {
	makeRequest();
});