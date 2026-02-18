function setBadge(riskLevel) {
  if (riskLevel === "Low Risk") {
    chrome.action.setBadgeText({ text: "SAFE" });
    chrome.action.setBadgeBackgroundColor({ color: "#16a34a" });
  } else if (riskLevel === "Suspicious") {
    chrome.action.setBadgeText({ text: "WARN" });
    chrome.action.setBadgeBackgroundColor({ color: "#facc15" });
  } else {
    chrome.action.setBadgeText({ text: "RISK" });
    chrome.action.setBadgeBackgroundColor({ color: "#dc2626" });
  }
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {

    fetch("http://localhost:5000/check-url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: tab.url })
    })
    .then(res => res.json())
    .then(data => {
      setBadge(data.risk_level);
    })
    .catch(err => console.error(err));

  }
});
