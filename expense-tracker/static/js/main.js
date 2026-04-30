// Video Modal Functionality
document.addEventListener('DOMContentLoaded', function() {
    const videoTriggerBtn = document.getElementById('videoTriggerBtn');
    const videoModal = document.getElementById('videoModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalOverlay = document.querySelector('.modal-overlay');
    const videoIframe = document.getElementById('videoIframe');

    // Open modal when "See how it works" button is clicked
    if (videoTriggerBtn) {
        videoTriggerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            videoModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        });
    }

    // Close modal when close button is clicked
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', function() {
            closeVideoModal();
        });
    }

    // Close modal when overlay is clicked
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function() {
            closeVideoModal();
        });
    }

    // Close modal when Escape key is pressed
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && videoModal.classList.contains('active')) {
            closeVideoModal();
        }
    });

    // Function to close modal and stop video
    function closeVideoModal() {
        videoModal.classList.remove('active');
        document.body.style.overflow = 'auto'; // Re-enable background scroll
        
        // Stop video by replacing src
        const currentSrc = videoIframe.src;
        videoIframe.src = '';
        videoIframe.src = currentSrc;
    }
});
