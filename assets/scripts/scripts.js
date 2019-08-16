$("#modelId").on("shown.bs.modal", function() {
	$.ajax({
		url: "/create",
		type: "get",
		dataType: "json",
		success: function(data) {
			$("#modelId .modal-body").html(data.html_form);
		}
	});
});

$(document).ready(function() {
	var showForm = function() {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: "get",
			dataType: "json",
			beforeSend: function() {
				$("#new-book-modal").modal("show");
			},
			success: function(data) {
				$("#new-book-modal .modal-content").html(data.html_form);
			}
		});
	};

	var saveForm = function() {
		var form = $(this);
		$.ajax({
			url: form.attr("data-url"),
			data: form.serialize(),
			type: form.attr("method"),
			dataType: "json",
			success: function(data) {
				if (data.is_valid) {
					$("#books-table tbody").html(data.book_list);
					$("#new-book-modal").modal("hide");
				} else {
					$("#new-book-modal .modal-content").html(data.html_form);
				}
			}
		});
		return false;
	};

	// book list
	$("#book-modal-btn").click(showForm);
	// new book
	$("#new-book-modal").on("submit", ".create-form", saveForm);
	//edit book
	$("#books-table").on("click", "#edit-modal-btn", showForm);
	// delete book
	$("#books-table").on("click", "#delete-modal-btn", showForm);
});
