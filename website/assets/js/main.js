$(document).ready(function() {
	$('.sidenav').sidenav();
	$('select').formSelect();
	$('#task').fadeOut(0);
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

function makeRequest() {

	M.Toast.dismissAll();

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

		M.toast({
			html: 'Prosim izberi predmet',
			classes: 'bigToast hide-on-med-and-down'
		})

		M.toast({
			html: 'Prosim izberi predmet',
			classes: 'smallToast hide-on-large-only'
		})

	} else {

		var requestUrl = $.param(req);
		requestUrl = "/api/naloga?"+requestUrl;
		console.log(requestUrl)

		$.getJSON(requestUrl, function(data) {
			setImageAndUrl("/api/image?i="+data["dodatno"], "/api/image?i="+data["img"], data["rešitve"], data["predmet"], data["leto"], data["rok"]);
			$("#task").fadeIn(200);
			return true;
		}).fail(function() {
			M.toast({
				html: '<span style="font-weight: bold;">Napaka!</span><span>&nbspPoskusi ponovno</span>',
				classes: 'bigToast hide-on-med-and-down'
			})

			M.toast({
				html: '<span style="font-weight: bold;">Napaka!</span><span>&nbspPoskusi ponovno</span>',
				classes: 'smallToast hide-on-large-only'
			})
			return false;
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
	if (makeRequest()) {
		setTimeout(function() {
			$('html, body').animate({
		        scrollTop: $("#task").offset().top
		    });
		}, 210);
	}
});

$(document).on("click","#newQuestion",function() {
	makeRequest();
});