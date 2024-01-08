const btnUpload = $("#upload_file");
const btnOuter = $(".button_outer");
const uploadContainer = $("#uploadContainer");

$(document).ready(function() {
    // Event delegation for dynamically added elements
    btnUpload.on('change', function(e) {
        handleFileUpload(e);
    });

    $(document).on('click', '.file_remove', function() {
        resetUpload();
    });

    $('#extractedTextForm').hide();
});

function handleFileUpload(e) {
    const file = e.target.files[0];
    const ext = file.name.split('.').pop().toLowerCase();
    if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) === -1) {
        $(".error_msg").text("Not an Image...");
    } else {
        $(".error_msg").text("");
        btnOuter.addClass("file_uploading");
        uploadFile(file);
    }
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    $.ajax({
        url: '/moana/ocr_openai_analysis',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: handleUploadSuccess,
        error: handleUploadError
    });

    displayUploadedFile(file);
}

function handleUploadSuccess(response) {

    // Hide the upload button
    btnOuter.removeClass("file_uploading").addClass("file_uploaded");
    btnOuter.hide();
    uploadContainer.hide();

    // populateExtractedText(response.extracted_text);
    populateListWithAnswers(response.answers);

    // Populate and show the extracted text area
    populateExtractedText(response.extracted_text);
    toggleExtractedTextVisibility(true);
    adjustTextareaHeightBasedOnContent();

}

function handleUploadError(jqXHR, textStatus, errorMessage) {
    console.log("Upload Error:", errorMessage);
    $(".error_msg").text('Error: ' + errorMessage);
    btnOuter.removeClass("file_uploading");
}

function displayUploadedFile(file) {
    const uploadedFile = URL.createObjectURL(file);
    $("#uploaded_view").html('<img src="' + uploadedFile + '" />').addClass("show");
    $("#uploaded_view").append('<span class="file_remove">X</span>');
}

function resetUpload() {
    $("#uploaded_view").removeClass("show").find("img").remove();
    $("#uploaded_view .file_remove").remove();
    $("#responseList").empty();
    $('#extractedTextForm').hide();
    $('#extractedText').val('');
    $(".error_msg").text("");

    // Reset the file input
    btnUpload.replaceWith(btnUpload.val('').clone(true));

    // Show the button and container again
    btnOuter.removeClass("file_uploading file_uploaded").show();
    uploadContainer.show();
}

function populateListWithAnswers(answers) {
    const responseList = $("#responseList");
    responseList.empty();

    answers.forEach(function(qa_pair) {
        const question = Object.keys(qa_pair)[0];
        const answer = qa_pair[question];

        const listItem = $('<li class="list-group-item"></li>');
        listItem.html('<strong>' + question + '</strong>: ' + answer);
        responseList.append(listItem);
    });
}


function adjustTextareaHeightBasedOnContent() {
    const textArea = $('#extractedText');
    // Adjust height based on scrollHeight or set a default
    const newHeight = textArea.get(0).scrollHeight || '100px';
    setExtractedTextHeight(newHeight);
}

function populateExtractedText(text) {
    // Populate the text area with extracted text
    if (text) {
        $('#extractedText').val(text);
        adjustTextareaHeightBasedOnContent(); // Adjust height after setting text
    } else {
        $('#extractedText').val('No OCR text available.');
        setExtractedTextHeight('100px'); // Set to default height
    }
}

function toggleExtractedTextVisibility(show) {
    if (show) {
        $('#extractedTextForm').show();
    } else {
        $('#extractedTextForm').hide();
    }
}

function setExtractedTextHeight(height) {
    $('#extractedText').css('height', height);
}
