function fakeUpload() {
    let fileInput = document.getElementById("fileInput");
    let resultText = document.getElementById("result");

    if (fileInput.files.length === 0) {
        resultText.innerText = "❌ Please select a file first.";
        return;
    }

    resultText.innerText = "⏳ Uploading... (Waiting for Backend)";
    
    setTimeout(() => {
        resultText.innerText = "✅ Fake Response: Authentication Successful (Replace when backend is ready)";
    }, 2000);
}
function uploadImage() {
    let fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("Please select an image.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/verify/", {  // Adjust URL based on your Django setup
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.message + " (Confidence: " + data.confidence + "%)";
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error processing image.";
    });
}
