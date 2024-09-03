document.getElementById('generate-btn').addEventListener('click', function() {
    // Fetch the YouTube link or file
    const youtubeLink = document.getElementById('youtube-link').value;
    const fileInput = document.getElementById('file-input').files[0];

    // Check if the YouTube link or file is provided
    if (youtubeLink || fileInput) {
        // Hide the input section and show the loading section
        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('loading-section').classList.remove('hidden');

        // Simulate a loading process (e.g., generating blog content)
        setTimeout(function() {
            document.getElementById('loading-section').classList.add('hidden');
            document.getElementById('result-section').classList.remove('hidden');
            document.getElementById('blog-output').innerText = "Here is the generated blog content...";

            // Display whether it was a YouTube link or a file
            if (youtubeLink) {
                document.getElementById('source-info').innerText = `Generated from YouTube link: ${youtubeLink}`;
            } else if (fileInput) {
                document.getElementById('source-info').innerText = `Generated from file: ${fileInput.name}`;
            }
        }, 3000); // Simulate a 3-second generation time

    } else {
        alert("Please provide a YouTube link or upload a file.");
    }
});

document.getElementById('regenerate-btn').addEventListener('click', function() {
    document.getElementById('input-section').classList.remove('hidden');
    document.getElementById('result-section').classList.add('hidden');
    document.getElementById('blog-output').innerText = '';
    document.getElementById('source-info').innerText = '';
});

document.getElementById('save-btn').addEventListener('click', function() {
    alert("Blog saved successfully!");
});

document.getElementById('delete-btn').addEventListener('click', function() {
    if (confirm("Are you sure you want to delete this blog?")) {
        document.getElementById('result-section').classList.add('hidden');
        document.getElementById('input-section').classList.remove('hidden');
        document.getElementById('blog-output').innerText = '';
        document.getElementById('source-info').innerText = '';
    }
});

document.getElementById('logout').addEventListener('click', function() {
    alert("Logged out successfully!");
    // Add actual logout functionality here
});

document.getElementById('view-tasks').addEventListener('click', function() {
    alert("Viewing all tasks...");
    // Add actual view tasks functionality here
});
