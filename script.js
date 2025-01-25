document.addEventListener("DOMContentLoaded", () => {
    const blogContainer = document.getElementById("blog-container");

    // Fetch posts from the JSON file
    fetch("posts.json")
        .then(response => response.json())
        .then(posts => {
            // Generate HTML for each post
            posts.forEach(post => {
                const postElement = document.createElement("div");
                postElement.classList.add("post");

                postElement.innerHTML = `
                    <h3>${post.title}</h3>
                    <p><em>${post.date}</em></p>
                    <p>${post.content}</p>
                `;

                blogContainer.appendChild(postElement);
            });
        })
        .catch(error => {
            console.error("Error loading posts:", error);
            blogContainer.innerHTML = "<p>Failed to load posts. Please try again later.</p>";
        });
});
document.addEventListener("DOMContentLoaded", () => {
    // Find all forms and their respective containers
    const commentForms = document.querySelectorAll(".comment-form");
    const commentsContainers = document.querySelectorAll(".comments-container");

    // Initialize comments for each article
    commentForms.forEach((form, index) => {
        const container = commentsContainers[index];
        const storageKey = `comments-article-${index}`;
        const comments = JSON.parse(localStorage.getItem(storageKey)) || [];

        // Display comments
        function displayComments() {
            container.innerHTML = "<h4>All Comments:</h4>";
            comments.forEach(comment => {
                const commentElement = document.createElement("div");
                commentElement.classList.add("comment");
                commentElement.innerHTML = `
                    <p><strong>${comment.username}:</strong> ${comment.text}</p>
                `;
                container.appendChild(commentElement);
            });
        }

        // Handle form submission
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const username = form.querySelector(".username").value.trim();
            const commentText = form.querySelector(".comment").value.trim();

            if (username && commentText) {
                comments.push({ username, text: commentText });
                localStorage.setItem(storageKey, JSON.stringify(comments));
                displayComments();
                form.reset();
            }
        });

        // Initial display of comments
        displayComments();
    });
});
