// app/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initAlerts();
});

// Alert message handling
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Auto dismiss alerts after 5 seconds
        setTimeout(() => {
            if (alert) {
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }
        }, 5000);
    });
}

// Format timestamp for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Format file size for display
function formatFileSize(bytes) {
    if (bytes < 1024) {
        return bytes + ' bytes';
    } else if (bytes < 1048576) {
        return (bytes / 1024).toFixed(2) + ' KB';
    } else {
        return (bytes / 1048576).toFixed(2) + ' MB';
    }
}

// Format duration for display
function formatDuration(seconds) {
    if (!seconds) return 'N/A';

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);

    if (minutes === 0) {
        return `${remainingSeconds} sec`;
    }

    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            // Show success message
            const copyMessage = document.createElement('div');
            copyMessage.className = 'copy-message';
            copyMessage.textContent = 'Copied to clipboard!';
            document.body.appendChild(copyMessage);

            setTimeout(() => {
                copyMessage.classList.add('show');
                setTimeout(() => {
                    copyMessage.classList.remove('show');
                    setTimeout(() => {
                        document.body.removeChild(copyMessage);
                    }, 300);
                }, 1500);
            }, 10);
        })
        .catch(err => {
            console.error('Failed to copy text: ', err);
        });
}