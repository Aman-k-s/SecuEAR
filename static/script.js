function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let resultText = document.getElementById("result");

    if (fileInput.files.length === 0) {
        resultText.textContent = "Please choose a file first.";
        return;
    }

    let formData = new FormData();
    formData.append("fileInput", fileInput.files[0]);

    fetch("/upload/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("temp_file_path").value = data.temp_file_path;  // Store path
            resultText.textContent = "File uploaded successfully!";
        } else {
            resultText.textContent = data.error;
        }
    })
    .catch(error => {
        resultText.textContent = "Upload failed!";
    });
}
