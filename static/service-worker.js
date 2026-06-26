async function fetchJSON(url, options = {}) {
    const response = await fetch(url, options);
    return response.json();
}

function showTab(id) {
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

async function loadStats() {
    const stats = await fetchJSON("/api/stats");
    const byLanguage = stats.by_language.map(row => `<li>${row.language}: ${row.total_minutes} min</li>`).join("");

    document.getElementById("stats").innerHTML = `
        <div class="grid">
            <div class="stat"><strong>Total Practice</strong><p>${stats.total_minutes} minutes</p></div>
            <div class="stat"><strong>Challenges</strong><p>${stats.completed_challenges} / ${stats.total_challenges}</p></div>
            <div class="stat"><strong>Portfolio Projects</strong><p>${stats.portfolio_count}</p></div>
            <div class="stat"><strong>By Language</strong><ul>${byLanguage || "<li>No sessions yet</li>"}</ul></div>
        </div>
    `;
}

async function loadRoadmap() {
    const roadmap = await fetchJSON("/api/roadmap");
    document.getElementById("roadmapList").innerHTML = roadmap.map(item => `
        <div class="item">
            <h3>Week ${item.week}: ${item.topic}</h3>
            <p><strong>${item.track}</strong></p>
            <p>${item.goal}</p>
        </div>
    `).join("");
}

async function loadChallenges() {
    const challenges = await fetchJSON("/api/challenges");

    document.getElementById("challengeList").innerHTML = challenges.map(challenge => `
        <div class="item ${challenge.completed ? "completed" : ""}">
            <h3>${challenge.title}</h3>
            <p><strong>${challenge.language}</strong></p>
            <p>${challenge.description}</p>
            <textarea id="answer-${challenge.id}" placeholder="Type your code or explanation here"></textarea>
            <br><br>
            <button onclick="checkAnswer(${challenge.id})">Check Answer</button>
            <button onclick="toggleChallenge(${challenge.id})">
                ${challenge.completed ? "Mark Incomplete" : "Mark Complete"}
            </button>
            <p id="check-${challenge.id}"></p>
        </div>
    `).join("");
}

async function checkAnswer(id) {
    const answer = document.getElementById(`answer-${id}`).value;

    const result = await fetchJSON("/api/check-answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({challenge_id: id, answer})
    });

    document.getElementById(`check-${id}`).textContent = result.message;
}

async function toggleChallenge(id) {
    await fetchJSON(`/api/challenges/${id}/toggle`, { method: "POST" });
    loadChallenges();
    loadStats();
}

async function runPython() {
    const code = document.getElementById("pythonCode").value;

    const result = await fetchJSON("/api/run-python", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code})
    });

    document.getElementById("pythonOutput").textContent = result.output;
}

function runJavaScript() {
    const code = document.getElementById("jsCode").value;
    const output = document.getElementById("jsOutput");
    output.textContent = "";

    try {
        new Function(code)();
    } catch (error) {
        output.textContent = error.name + ": " + error.message;
    }
}

async function runSQL() {
    const query = document.getElementById("sqlCode").value;

    const result = await fetchJSON("/api/run-sql", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query})
    });

    const message = document.getElementById("sqlMessage");
    const output = document.getElementById("sqlOutput");

    if (!result.ok) {
        message.textContent = result.error;
        output.innerHTML = "";
        return;
    }

    message.textContent = result.message;

    if (!result.columns.length) {
        output.innerHTML = "";
        return;
    }

    const header = result.columns.map(col => `<th>${col}</th>`).join("");
    const rows = result.rows.map(row => {
        return `<tr>${row.map(value => `<td>${value}</td>`).join("")}</tr>`;
    }).join("");

    output.innerHTML = `<table><thead><tr>${header}</tr></thead><tbody>${rows}</tbody></table>`;
}

async function loadSessions() {
    const sessions = await fetchJSON("/api/sessions");

    if (sessions.length === 0) {
        document.getElementById("sessions").innerHTML = "<p>No sessions yet.</p>";
        return;
    }

    document.getElementById("sessions").innerHTML = sessions.map(session => `
        <div class="item">
            <h3>${session.language}: ${session.topic}</h3>
            <p>${session.minutes} minutes</p>
            <p>${session.notes || ""}</p>
            <small>${session.created_at}</small>
        </div>
    `).join("");
}

document.getElementById("sessionForm").addEventListener("submit", async event => {
    event.preventDefault();

    const data = {
        language: document.getElementById("language").value,
        topic: document.getElementById("topic").value,
        minutes: document.getElementById("minutes").value,
        notes: document.getElementById("notes").value
    };

    const result = await fetchJSON("/api/sessions", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    document.getElementById("sessionMessage").textContent = result.error || result.message;
    event.target.reset();
    loadStats();
    loadSessions();
});

async function loadProjectIdeas() {
    const projects = await fetchJSON("/api/projects");

    document.getElementById("projectIdeas").innerHTML = projects.map(project => `
        <div class="item">
            <h3>${project.title}</h3>
            <p><strong>Skills:</strong> ${project.skills}</p>
            <p>${project.description}</p>
            <ul>${project.features.map(feature => `<li>${feature}</li>`).join("")}</ul>
        </div>
    `).join("");
}

async function loadPortfolio() {
    const projects = await fetchJSON("/api/portfolio");

    if (projects.length === 0) {
        document.getElementById("portfolioList").innerHTML = "<p>No saved projects yet.</p>";
        return;
    }

    document.getElementById("portfolioList").innerHTML = projects.map(project => `
        <div class="item">
            <h3>${project.title}</h3>
            <p><strong>Status:</strong> ${project.status}</p>
            <p>${project.notes || ""}</p>
            <small>${project.created_at}</small>
        </div>
    `).join("");
}

document.getElementById("portfolioForm").addEventListener("submit", async event => {
    event.preventDefault();

    const data = {
        title: document.getElementById("projectTitle").value,
        status: document.getElementById("projectStatus").value,
        notes: document.getElementById("projectNotes").value
    };

    const result = await fetchJSON("/api/portfolio", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    document.getElementById("portfolioMessage").textContent = result.error || result.message;
    event.target.reset();
    loadPortfolio();
    loadStats();
});

loadStats();
loadRoadmap();
loadChallenges();
loadSessions();
loadProjectIdeas();
loadPortfolio();


// PWA registration
if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("/service-worker.js")
            .catch(error => console.log("Service worker registration failed:", error));
    });
}

let deferredInstallPrompt = null;

window.addEventListener("beforeinstallprompt", event => {
    event.preventDefault();
    deferredInstallPrompt = event;

    if (!document.getElementById("installButton")) {
        const button = document.createElement("button");
        button.id = "installButton";
        button.textContent = "Install App";
        button.style.margin = "10px";
        button.onclick = async () => {
            if (!deferredInstallPrompt) return;
            deferredInstallPrompt.prompt();
            await deferredInstallPrompt.userChoice;
            deferredInstallPrompt = null;
            button.remove();
        };
        document.querySelector("header").appendChild(button);
    }
});
