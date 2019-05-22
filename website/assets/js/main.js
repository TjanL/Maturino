$(document).ready(function() {
	$('.sidenav').sidenav();
	$('select').formSelect();
	$('#math').fadeOut(0);
	$('#slovene').fadeOut(0);
	$('#unsetModal').modal();
	$('#errorModal').modal();
	$('#levelModal').modal();
});

function fadeIn(subject) {
	if (subject == "slovenščina") {
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

	var req = {
		subject:$('#predmet').val(),
		level:$('#raven').val(),
		year:$('#leto').val(),
		term:$('#rok').val()
	}

	var showSubject = req.subject;

	if (showSubject == "unset") {

		$('#unsetModal').modal('open');

	} else {

		if (req.level == "or" && req.subject == "slovenscina") {
			$('#levelModal').modal('open');
		} else {
			var requestUrl = $.param(req);
			requestUrl = "/api/naloga?"+requestUrl;
			console.log(requestUrl)

			$.getJSON(requestUrl, function(data) {
				setImageAndUrl(data.Dodatno, data.Path, data.Rešitve);
				fadeIn(showSubject);
			}).fail(function() {
				$('#errorModal').modal('open');
			});
		}

	}
}

function setImageAndUrl(addPath, exPath, url) {
	$('#dodatno').attr("src",addPath);
	$('#naloga').attr("src", exPath);
	$('#resitve').attr("href", url);
}

$(document).on("click","#show",function() {
	makeRequest();
});