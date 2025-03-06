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
