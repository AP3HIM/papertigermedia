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
