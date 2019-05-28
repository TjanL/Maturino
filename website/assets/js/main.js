$('.sidenav').sidenav();
$('select').formSelect();
$('.materialboxed').materialbox();
$("#disclaimerModal").modal();

$("#predmet").change(function() {
	var options = {
		"slovenščina": "vr"
	}

	$("#raven").html("");
	var predmet = $("#predmet").val();
	if (predmet in options) {
		var full_name = options[predmet] == "or" ? "Osnovna" : "Višja";
		$("#raven").append("<option value='" + options[predmet] + "' selected>" + full_name + "</option>");

	} else {
		$("#raven").append("<option value='' selected>Naključno</option>");
		$("#raven").append("<option value='or'>Osnovna</option>");
		$("#raven").append("<option value='vr'>Višja</option>");
	}
	$("#raven").formSelect();
})

$("#Show, #ShowNew").click(function() {
	var req = {};
	if ($('#predmet').val()) {
		req["subject"] = $('#predmet').val();
	}
	if ($('#raven').val()) {
		req["level"] = $('#raven').val();
	}
	if ($('#leto').val()) {
		req["year"] = $('#leto').val();
	}
	if ($('#rok').val()) {
		req["term"] = $('#rok').val();
	}

	if ($('#predmet').val() == null) {
		M.toast({
			html: 'Prosim izberi predmet',
			classes: 'toast'
		})
	} else {
		$.get({
			url: "/api/naloga?" + $.param(req),
			success: function(data) {
				$('#maturaInfo').text(data["predmet"] + ", " + data["rok"] + " " + data["leto"]);

				$('#img-priloga').attr("src", "/api/image?i=" + data["dodatno"]);
				$('#img-naloga').attr("src", "/api/image?i=" + data["img"]);
				$('#resitve').attr("href", data["rešitve"]);

				$('.img-area').scrollTop(0);
				
				$("#Task").fadeIn(200);

				$("body, html").animate({
					scrollTop: $("#maturaInfo").offset().top,
					duration: 1000
				});
			},
			error: function() {
				M.toast({
				html: '<span style="font-weight: bold;">Napaka!</span><span>&nbspPoskusi ponovno</span>',
				classes: 'toast'
				})
			},
			dataType: "json"
		});
	}
})
