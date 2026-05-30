
document.addEventListener("DOMContentLoaded", () => {
  const cursor = document.querySelector(".cursor");

  if (!cursor) {
    console.error("Error: Could not find the .cursor div!");
    return;
  }


  document.addEventListener("mousemove", (e) => {
    const width = 70;
    const height = 70;

    cursor.style.left = `${e.clientX - width / 2}px`;
    cursor.style.top = `${e.clientY - height / 2}px`;
  });

  document.addEventListener('mousedown', () => {
    cursor.classList.add('is-clicked');
  });

  document.addEventListener('mouseup', () => {
    cursor.classList.remove('is-clicked');
  });
});