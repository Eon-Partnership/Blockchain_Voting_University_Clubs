 document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("voteForm").addEventListener("submit", function(event) {
        event.preventDefault();

        const token = document.getElementById("token").value;
        selectedElement = document.getElementById("candidate")
        const candidate = (selectedElement.options[selectedElement.selectedIndex]).textContent;
        const candidateId = selectedElement.value

        fetch('/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token: token, candidate: candidate, candidateId: candidateId })
        })
        .then(response => {
            if (response.ok) {
                alert("Vote submitted successfully");
            } else {
                throw new Error('Vote submission failed');
            }
        })
        .catch(error => {
            console.error('Vote submission error:', error);
            alert("Failed to submit vote. Please try again later.");
        });
    });
});