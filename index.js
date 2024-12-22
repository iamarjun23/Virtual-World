document.addEventListener("DOMContentLoaded", function () {
    const leftButton = document.querySelector(".left-button");
    const rightButton = document.querySelector(".right-button");
    const textItems = document.querySelectorAll(".text-item");
    let currentIndex = 0;

    // Function to show the text at the current index
    function showText(index) {
        console.log(`Showing text at index: ${index}`);  // Logs when a new text is shown
        // Hide all text items
        textItems.forEach((item) => item.classList.remove("active"));
        
        // Show the active text item
        textItems[index].classList.add("active");

        console.log(`Text content: ${textItems[index].querySelector(".text-content").textContent}`);  // Logs the content of the active text
    }

    // Initial display of the first text item
    showText(currentIndex);

    // Move to the previous text item when the left button is clicked
    leftButton.addEventListener("click", function (e) {
        e.preventDefault();
        console.log("Left button clicked"); // Log when the left button is clicked

        currentIndex = (currentIndex === 0) ? textItems.length - 1 : currentIndex - 1;
        showText(currentIndex);
    });

    // Move to the next text item when the right button is clicked
    rightButton.addEventListener("click", function (e) {
        e.preventDefault();
        console.log("Right button clicked"); // Log when the right button is clicked

        currentIndex = (currentIndex === textItems.length - 1) ? 0 : currentIndex + 1;
        showText(currentIndex);
    });

    // Automatically switch between text items every 5 seconds
    setInterval(function () {
        console.log("Auto switching text...");  // Log when the text switches automatically
        currentIndex = (currentIndex === textItems.length - 1) ? 0 : currentIndex + 1;
        showText(currentIndex);
    }, 5000); // Change every 5 seconds
});
