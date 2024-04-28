document.getElementById('video-thumbnail').addEventListener('change', function (event) {
    const thumbnailPreview = document.getElementById('thumbnail-preview');
    const file = event.target.files[0];
    if (file) {
        thumbnailPreview.src = URL.createObjectURL(file);
        thumbnailPreview.classList.remove('hidden');
    } else {
        // Reset the preview if no file is selected
        thumbnailPreview.src = '#';
    }
});