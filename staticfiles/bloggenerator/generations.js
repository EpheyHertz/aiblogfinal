document.addEventListener('DOMContentLoaded', () => {
    const backButton = document.getElementById('back');
    const regenerateButton = document.querySelector('.regenerate-btn');
    const saveButton = document.querySelector('.save-btn');
    const deleteButton = document.querySelector('.delete-btn');

    backButton.addEventListener('click', () => {
        window.location.href = 'allblogspost.html'; // Replace with the actual path to the all blogs page
    });

    regenerateButton.addEventListener('click', () => {
        alert('Regenerate button clicked!');
        // Implement the regenerate logic here
    });

    saveButton.addEventListener('click', () => {
        alert('Save button clicked!');
        // Implement the save logic here
    });

    deleteButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to delete this blog?')) {
            alert('Blog deleted!');
            // Implement the delete logic here
        }
    });

    // Example for setting the source dynamically (YouTube link or uploaded file)
    const isYouTubeLink = true; // Change this based on your logic
    const sourceLink = document.getElementById('source-link');
    if (isYouTubeLink) {
        sourceLink.href = 'https://www.youtube.com/watch?v=example'; // Replace with actual link
        sourceLink.textContent = 'YouTube Link';
    } else {
        document.getElementById('blog-source').textContent = 'Source: Uploaded from local files';
    }
});
