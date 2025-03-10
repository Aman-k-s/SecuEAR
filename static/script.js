function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let resultText = document.getElementById("result");

    // Check if a file is selected
    if (fileInput.files.length === 0) {
        resultText.innerText = "Please select a file before uploading.";
        resultText.classList.remove("text-green-400");
        resultText.classList.add("text-red-400");
        return;
    }

    let file = fileInput.files[0];

    // Check if the file has a .ply extension
    if (!file.name.toLowerCase().endsWith(".ply")) {
        resultText.innerText = "Only .ply files are allowed!";
        resultText.classList.remove("text-green-400");
        resultText.classList.add("text-red-400");
        fileInput.value = "";  // Reset file input
        return;
    }

    let formData = new FormData();
    formData.append("fileInput", file);

    fetch("/upload/", {  // Backend route to handle file upload
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            resultText.innerText = "File uploaded successfully!";
            resultText.classList.remove("text-red-400");
            resultText.classList.add("text-green-400");
        } else {
            resultText.innerText = "Upload failed: " + data.error;
            resultText.classList.remove("text-green-400");
            resultText.classList.add("text-red-400");
        }
    })
    .catch(error => {
        resultText.innerText = "An error occurred while uploading.";
        resultText.classList.remove("text-green-400");
        resultText.classList.add("text-red-400");
    });
}
