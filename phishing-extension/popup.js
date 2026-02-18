function normalizeDomain(url) {
  try {
    let u = new URL(url);
    let domain = u.hostname.replace(/^www\./, "");
    return domain;
  } catch {
    return url;
  }
}

chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {

  const currentUrl = tabs[0].url;
  const domain = normalizeDomain(currentUrl);

  document.getElementById("domain").textContent = domain;

  chrome.storage.local.get(["trustedSites"], function(result) {

    let trusted = result.trustedSites || [];

    if (trusted.includes(domain)) {
      showTrusted(domain);
      return;
    }

    // Not trusted → check API
    fetch("http://localhost:5000/check-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: currentUrl })
    })
    .then(res => res.json())
    .then(data => showRisk(data, domain));

  });
});

function showTrusted(domain) {
  const statusBox = document.getElementById("statusBox");

  statusBox.innerHTML = `
    <p style="color:#16a34a;font-weight:bold;">
      ✔ Trusted by You
    </p>
    <button id="removeTrust" style="
        margin-top:10px;
        background:#374151;
        color:white;
        border:none;
        padding:6px;
        border-radius:6px;
        cursor:pointer;
    ">
      Remove Trust
    </button>
  `;

  document.querySelector(".buttons").style.display = "none";

  document.getElementById("removeTrust").onclick = function() {
    chrome.storage.local.get(["trustedSites"], function(result) {
      let trusted = result.trustedSites || [];

      trusted = trusted.filter(site => site !== domain);

      chrome.storage.local.set({ trustedSites: trusted }, function() {
        location.reload(); // Reload popup to re-check risk
      });
    });
  };
}


function showRisk(data, domain) {

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

  document.getElementById("markSafe").onclick = function() {
    chrome.storage.local.get(["trustedSites"], function(result) {
      let trusted = result.trustedSites || [];
      trusted.push(domain);
      chrome.storage.local.set({ trustedSites: trusted });
      showTrusted(domain);
    });
  };

  document.getElementById("markPhishing").onclick = function() {
    document.getElementById("feedbackStatus").textContent = "Feedback recorded!";
    sendFeedback(domain, "phishing");
  };
}

function sendFeedback(url, label) {
  fetch("http://localhost:5000/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: url, label: label })
  });
}
