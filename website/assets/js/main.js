function gen_option(text, value=null) {
	if (value == null) value = text;
	return "<option value='" + value + "'>" + text + "</option>";
}

$('.sidenav').sidenav();
$('select').formSelect();
$('.materialboxed').materialbox();
$("#disclaimerModal").modal();

var options;
$.get({
	url: "/api/options",
	success: function(data) {
		options = data;
		var predmeti = Object.keys(data);
		for (var i = 0; i < predmeti.length; i++) {
			$("#Predmet").append(gen_option(predmeti[i]));
		}
		$("#Predmet").formSelect();
	},
	dataType: "json"
});

$("#Predmet").change(function() {
	var full_name = {
		"or": "Osnovna",
		"vr": "Višja",
		"jesen": "Jesenski",
		"pomlad": "Spomladanski"
	}

	var predmet = $("#Predmet").val();
	var option_keys = Object.keys(options[predmet]);
	for (var n = 0; n < option_keys.length; n++) {
		$("#" + option_keys[n]).html("");
		if (options[predmet][option_keys[n]].length > 1) {
			$("#" + option_keys[n]).append(gen_option("Naključno", ""));
		}
		for (var i = 0; i < options[predmet][option_keys[n]].length; i++) {
			var value = options[predmet][option_keys[n]][i];
			var text = Object.keys(full_name).includes(value) ? full_name[value] : value;
			$("#" + option_keys[n]).append(gen_option(text, value));
		}
		$("#" + option_keys[n]).formSelect();
	}
})

$("#Show, #ShowNew").click(function() {
	if ($('#Predmet').val() == null) {
		M.toast({
			html: 'Prosim izberi predmet',
			classes: 'toast'
		})
	} else {
		var req = {};
		if ($('#Predmet').val()) {
			req["subject"] = $('#Predmet').val();
		}
		if ($('#Nivo').val()) {
			req["level"] = $('#Nivo').val();
		}
		if ($('#Leto').val()) {
			req["year"] = $('#Leto').val();
		}
		if ($('#Rok').val()) {
			req["term"] = $('#Rok').val();
		}
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
