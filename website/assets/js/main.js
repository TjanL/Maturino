$(document).ready(function() {
	$('.sidenav').sidenav();
	$('select').formSelect();
	$('#math').fadeOut(0);
	$('#slovene').fadeOut(0);
	$('#unsetModal').modal();
	$('#errorModal').modal();
	$("#predmet").change(function() {
		setOptions();
	})
	setOptions();
});

$("a[href^='#']").click(function(e) {
	e.preventDefault();
	
	var position = $($(this).attr("href")).offset().top;

	$("body, html").animate({
		scrollTop: position
	});
});

function setOptions() {
	if ($("#predmet").val() == "slovenščina") {
		$(".unset").removeAttr("selected");
		$(".matematikaRaven").remove();
		$("#raven").append("<option value='vr' selected class='white slovenscinaRaven'>Višja</option>");
		$("#raven").formSelect();
	} else {
		$(".slovenscinaRaven").remove();
		$(".matematikaRaven").remove();
		$("#raven").append("<option value='or' class='white matematikaRaven'>Osnovna</option><option value='vr' class='white matematikaRaven'>Višja</option>");
		$("#raven").formSelect();
	}
}

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

	var req = {};

	if ($('#predmet').val() != "unset") {
		req["subject"] = $('#predmet').val();
	}
	if ($('#raven').val() != "unset") {
		req["level"] = $('#raven').val();
	}
	if ($('#leto').val() != "unset") {
		req["year"] = $('#leto').val();
	}
	if ($('#rok').val() != "unset") {
		req["term"] = $('#rok').val();
	}


	var showSubject = $('#predmet').val();

	if (showSubject == "unset") {

		$('#unsetModal').modal('open');

	} else {

		var requestUrl = $.param(req);
		requestUrl = "/api/naloga?"+requestUrl;
		console.log(requestUrl)

		$.getJSON(requestUrl, function(data) {
			setImageAndUrl("/api/image?i="+data["dodatno"], "/api/image?i="+data["img"], data["rešitve"], data["predmet"], data["leto"], data["rok"]);
			fadeIn(showSubject);
		}).fail(function() {
			$('#errorModal').modal('open');
		});

	}
}

function setImageAndUrl(addPath, exPath, url, subject, year, term) {
	$(".preloader-wrapper").removeClass("hide");
	$(".besedilo").addClass("loading");
	$(".loaderWrapper").removeClass("hide");

	$('#dodatno').attr("src",addPath);
	$('#naloga').attr("src", exPath);
	$('#resitve').attr("href", url);

	$('.besedilo').scrollTop(0);

	$("#dodatno").on("load",function() {
		$(".preloader-wrapper").addClass("hide");
		$(".besedilo").removeClass("loading");
		$(".loaderWrapper").addClass("hide");
	});

	$('.maturaInfo').text(subject+" "+year+" "+term);
}

$(document).on("click","#show",function() {
	makeRequest();
	setTimeout(function() {
		$('html, body').animate({
	        scrollTop: $("#slovene").offset().top
	    });
	}, 500);
});

$(document).on("click","#newQuestion",function() {
	makeRequest();
});