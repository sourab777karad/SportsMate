let isSpinning = false;
const coin = document.getElementById("coin");
const spinButton = document.getElementById("spin-btn");
const resultContainer = document.getElementById("result");
const resultText = document.getElementById("result-text");

// Spin/Stop Logic
spinButton.addEventListener("click", () => {
    if (!isSpinning) {
        // Start Spinning
        coin.style.animation = "spin 2s infinite linear";
        spinButton.textContent = "Stop";
        isSpinning = true;
        resultContainer.style.display = "none"; // Hide result during spin
    } else {
        // Stop Spinning
        coin.style.animation = "none";

        // Randomly Decide Winner
        const team1 = "{{ match_data['team1'] }}";
        const team2 = "{{ match_data['team2'] }}";
        const winner = Math.random() < 0.5 ? team1 : team2;

        // Show Result
        resultText.textContent = `${winner} won the toss!`;
        resultContainer.style.display = "block";
        spinButton.textContent = "Spin Again";
        isSpinning = false;
    }
});
