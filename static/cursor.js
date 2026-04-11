// cursor.js
document.addEventListener("DOMContentLoaded", () => {
    const cursor = document.querySelector(".cursor");

    if (!cursor) {
        console.error("Error: Could not find the .cursor div!");
        return;
    }

    console.log("Cursor script loaded successfully!");

    document.addEventListener("mousemove", (e) => {
        const width = 20; 
        const height = 20;
        
        cursor.style.left = `${e.clientX - width / 2}px`;
        cursor.style.top = `${e.clientY - height / 2}px`;
    });
});