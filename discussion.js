document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("discussion-form");
    const postsContainer = document.getElementById("discussion-posts");

    // Load existing posts from localStorage
    const posts = JSON.parse(localStorage.getItem("posts")) || [];

    // Display posts
    function displayPosts() {
        postsContainer.innerHTML = "<h3>Recent Posts</h3>";
        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.classList.add("post");
            postElement.innerHTML = `
                <p><strong>${post.username}:</strong> ${post.message}</p>
            `;
            postsContainer.appendChild(postElement);
        });
    }

    // Handle form submission
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value.trim();
        const message = document.getElementById("message").value.trim();

        if (username && message) {
            posts.push({ username, message });
            localStorage.setItem("posts", JSON.stringify(posts));
            displayPosts();
            form.reset();
        }
    });

    // Initial display
    displayPosts();
});
