document.addEventListener("DOMContentLoaded", () => {
  const chatWindow = document.getElementById("chatWindow");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");

  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.innerHTML = `<p><strong>${sender === "user" ? "You" : "AI"}:</strong> ${text}</p>`;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function fakeAIResponse(userMessage) {
    const responses = [
      "I see, tell me more about the problem 👀",
      "That sounds tricky. Did you try checking API docs?",
      "Interesting! Let’s try breaking it down step by step 🔍",
      "Hmm, maybe rate limiting is the issue 🤔",
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  }

  function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    userInput.value = "";

    // Fake AI response after 1 sec
    setTimeout(() => {
      const aiReply = fakeAIResponse(text);
      addMessage(aiReply, "bot");
    }, 1000);

     // Send user message to backend
    // try {
    //     const response = await fetch("/get_response", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ message: text })
    //     });
    //     const data = await response.json();
    //     addMessage(data.reply, "bot");
    // } catch (err) {
    //     addMessage("Error getting response from AI.", "bot");
    //     console.error(err);
    // }
  }

  // 🔹 Button click
  sendBtn.addEventListener("click", handleSend);

  // 🔹 Press Enter key
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // stop form submit
      handleSend();
    }
  });
});
