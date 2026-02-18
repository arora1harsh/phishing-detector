chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {

  const currentUrl = tabs[0].url;
  document.getElementById("domain").textContent = currentUrl;

  fetch("http://localhost:5000/check-url", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: currentUrl })
  })
  .then(res => res.json())
  .then(data => {

    const risk = document.getElementById("risk");
    const progress = document.getElementById("progress");

    risk.textContent = data.risk_level + 
      " (" + data.phishing_probability + "%)";

    progress.style.width = data.phishing_probability + "%";

    if (data.risk_level === "Low Risk") {
      progress.style.backgroundColor = "#16a34a";
    } else if (data.risk_level === "Suspicious") {
      progress.style.backgroundColor = "#facc15";
    } else {
      progress.style.backgroundColor = "#dc2626";
    }

    // Feedback buttons
    document.getElementById("markSafe").onclick = function() {
      sendFeedback(currentUrl, "safe");
    };

    document.getElementById("markPhishing").onclick = function() {
      sendFeedback(currentUrl, "phishing");
    };

  });

});


function sendFeedback(url, label) {
  fetch("http://localhost:5000/feedback", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: url, label: label })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("feedbackStatus").textContent =
      "Feedback submitted";
  })
  .catch(err => {
    document.getElementById("feedbackStatus").textContent =
      "Error submitting feedback";
  });
}
