function downloadFile(url, filename) {
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;  // Suggested filename for download
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
