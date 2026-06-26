let currentProblems=[];let currentIndex=0;
function showTab(id){document.querySelectorAll(".tab").forEach(t=>t.classList.remove("active"));document.getElementById(id).classList.add("active")}
async function fetchJSON(url,options={}){const r=await fetch(url,options);return r.json()}
async function loadStats(){const s=await fetchJSON("/api/stats");const by=s.by_language.map(x=>`<li>${x.language}: ${x.completed} completed</li>`).join("");const domains=s.by_domain.map(x=>`<div class="domain-item"><strong>${x.language}</strong><br>${x.domain}: ${x.completed}</div>`).join("");document.getElementById("stats").innerHTML=`<div class="grid"><div class="stat"><strong>Study Time</strong><p>${s.total_minutes} minutes</p></div><div class="stat"><strong>Total Problems Completed</strong><p>${s.completed_problems} / ${s.total_problems}</p></div><div class="stat"><strong>Completed by Language</strong><ul>${by||"<li>No problems completed yet</li>"}</ul></div></div><h3>Domain Progress</h3><div class="domain-grid">${domains||"<p>No domain progress yet.</p>"}</div>`}
async function loadDomainsAndPractice(){const l=document.getElementById("practiceLanguage").value;const domains=await fetchJSON(`/api/domains?language=${l}`);const box=document.getElementById("practiceDomain");box.innerHTML='<option>All</option>'+domains.map(d=>`<option>${d}</option>`).join("");loadPractice()}
async function loadPractice(){const l=document.getElementById("practiceLanguage").value;const d=document.getElementById("practiceDifficulty").value;const domain=document.getElementById("practiceDomain").value;currentProblems=await fetchJSON(`/api/practice?language=${encodeURIComponent(l)}&difficulty=${encodeURIComponent(d)}&domain=${encodeURIComponent(domain)}`);currentIndex=0;renderProblem()}
function renderProblem(){const box=document.getElementById("problemBox");if(!currentProblems.length){box.innerHTML="<p>No problems found.</p>";return}const p=currentProblems[currentIndex];box.innerHTML=`<h3>${p.title}</h3><p><span class="badge">${p.language}</span><span class="badge">${p.difficulty}</span><span class="badge">${p.domain}</span><span class="badge">Problem ${currentIndex+1} of ${currentProblems.length}</span></p><p>${p.prompt}</p><h4>Starter Code</h4><textarea id="practiceAnswer" class="answer-box">${p.starter}</textarea><br><br>${p.language==="Python"?`<button onclick="copyToPython()">Try in Python Lab</button>`:""}${p.language==="JavaScript"?`<button onclick="copyToJS()">Try in JavaScript Lab</button>`:""}${p.language==="SQL"?`<button onclick="copyToSQL()">Try in SQL Lab</button>`:""} <button onclick="checkPractice(${p.id})">Check Answer</button> <button onclick="showHint()">Show Hint</button> <button onclick="nextProblem()">Next Problem</button><p id="practiceFeedback"></p>`}
function nextProblem(){if(!currentProblems.length)return;currentIndex=(currentIndex+1)%currentProblems.length;renderProblem()}
function showHint(){document.getElementById("practiceFeedback").textContent="Hint: "+currentProblems[currentIndex].hint}
async function checkPractice(id){const answer=document.getElementById("practiceAnswer").value;const r=await fetchJSON("/api/check-practice",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({problem_id:id,answer})});document.getElementById("practiceFeedback").textContent=r.message;loadStats()}
function copyToPython(){document.getElementById("pythonCode").value=document.getElementById("practiceAnswer").value;showTab("python")}
function copyToJS(){document.getElementById("jsCode").value=document.getElementById("practiceAnswer").value;showTab("javascript")}
function copyToSQL(){document.getElementById("sqlCode").value=document.getElementById("practiceAnswer").value;showTab("sql")}
async function runPython(){const code=document.getElementById("pythonCode").value;const r=await fetchJSON("/api/run-python",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code})});document.getElementById("pythonOutput").textContent=r.output}
function runJavaScript(){const code=document.getElementById("jsCode").value;const out=document.getElementById("jsOutput");out.textContent="";try{new Function(code)()}catch(e){out.textContent=`${e.name}: ${e.message}`}}
async function runSQL(){const query=document.getElementById("sqlCode").value;const r=await fetchJSON("/api/run-sql",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query})});const msg=document.getElementById("sqlMessage");const out=document.getElementById("sqlOutput");if(!r.ok){msg.textContent=r.error;out.innerHTML="";return}msg.textContent=r.message;if(!r.columns.length){out.innerHTML="";return}const h=r.columns.map(c=>`<th>${c}</th>`).join("");const rows=r.rows.map(row=>`<tr>${row.map(v=>`<td>${v}</td>`).join("")}</tr>`).join("");out.innerHTML=`<table><thead><tr>${h}</tr></thead><tbody>${rows}</tbody></table>`}
document.getElementById("sessionForm").addEventListener("submit",async e=>{e.preventDefault();const data={language:document.getElementById("language").value,topic:document.getElementById("topic").value,minutes:document.getElementById("minutes").value,notes:document.getElementById("notes").value};const r=await fetchJSON("/api/sessions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});document.getElementById("sessionMessage").textContent=r.error||r.message;e.target.reset();loadStats();loadSessions()})
async function loadSessions(){const sessions=await fetchJSON("/api/sessions");const box=document.getElementById("sessionList");if(!sessions.length){box.innerHTML="<p>No sessions yet.</p>";return}box.innerHTML=sessions.map(s=>`<div class="problem-box"><strong>${s.language}: ${s.topic}</strong><p>${s.minutes} minutes</p><p>${s.notes||""}</p><small>${s.created_at}</small></div>`).join("")}
if("serviceWorker"in navigator){window.addEventListener("load",()=>{navigator.serviceWorker.register("/service-worker.js").catch(()=>{})})}
loadStats();loadDomainsAndPractice();loadSessions();

async function askTutor(){
    const question = document.getElementById("tutorQuestion").value;
    const context = document.getElementById("tutorContext").value;
    const result = await fetchJSON("/api/ask", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({question, context})
    });
    document.getElementById("tutorAnswer").textContent = result.answer;
}


let guidedLessons = [];
let currentGuidedLesson = null;
let currentGuidedStep = 0;

async function loadGuidedLessons(){
    const language = document.getElementById("guidedLanguage").value;
    guidedLessons = await fetchJSON(`/api/guided-lessons?language=${encodeURIComponent(language)}`);
    const select = document.getElementById("guidedLessonSelect");
    select.innerHTML = guidedLessons.map(lesson => `<option value="${lesson.id}">${lesson.title}</option>`).join("");
    selectGuidedLesson();
}

function selectGuidedLesson(){
    const lessonId = document.getElementById("guidedLessonSelect").value;
    currentGuidedLesson = guidedLessons.find(lesson => lesson.id === lessonId);
    currentGuidedStep = 0;
    renderGuidedStep();
}

function renderGuidedStep(){
    const box = document.getElementById("guidedLessonBox");
    if(!currentGuidedLesson){
        box.innerHTML = "<p>No guided lesson found.</p>";
        return;
    }

    const step = currentGuidedLesson.steps[currentGuidedStep];
    const isFinal = step.mode === "final";
    const isLearn = step.mode === "learn";

    box.innerHTML = `
        <h3>${currentGuidedLesson.title}</h3>
        <p><span class="badge">${currentGuidedLesson.language}</span><span class="badge">Step ${currentGuidedStep + 1} of ${currentGuidedLesson.steps.length}</span><span class="badge">${step.mode}</span></p>
        <h4>${step.title}</h4>
        <p>${step.explanation}</p>
        ${step.prompt ? `<p><strong>Your task:</strong> ${step.prompt}</p>` : ""}
        <textarea id="guidedAnswer" class="answer-box">${step.code || ""}</textarea>
        <br><br>
        ${currentGuidedLesson.language === "Python" ? `<button onclick="copyGuidedToPython()">Run in Python Lab</button>` : ""}
        ${currentGuidedLesson.language === "JavaScript" ? `<button onclick="copyGuidedToJS()">Run in JavaScript Lab</button>` : ""}
        ${currentGuidedLesson.language === "SQL" ? `<button onclick="copyGuidedToSQL()">Run in SQL Lab</button>` : ""}
        <button onclick="checkGuidedStep()">Check Step</button>
        <button onclick="showGuidedHint()">Hint</button>
        ${isLearn ? `<p><em>This is a learning step. Read it, run it, then continue.</em></p>` : ""}
        ${isFinal ? `<p><strong>Final challenge:</strong> Complete the full script without copying earlier steps.</p>` : ""}
        <p id="guidedFeedback"></p>
    `;
    syncGuidedStepType();
}

function nextGuidedStep(){
    if(!currentGuidedLesson) return;
    currentGuidedStep = Math.min(currentGuidedStep + 1, currentGuidedLesson.steps.length - 1);
    renderGuidedStep();
}

function previousGuidedStep(){
    if(!currentGuidedLesson) return;
    currentGuidedStep = Math.max(currentGuidedStep - 1, 0);
    renderGuidedStep();
}

function showGuidedHint(){
    const step = currentGuidedLesson.steps[currentGuidedStep];
    document.getElementById("guidedFeedback").textContent = "Hint: " + (step.hint || "Run the code and read the explanation.");
}

async function checkGuidedStep(){
    const answer = document.getElementById("guidedAnswer").value;
    const result = await fetchJSON("/api/check-guided-step", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            lesson_id: currentGuidedLesson.id,
            step_index: currentGuidedStep,
            answer
        })
    });
    document.getElementById("guidedFeedback").textContent = result.message;
}

function copyGuidedToPython(){
    document.getElementById("pythonCode").value = document.getElementById("guidedAnswer").value;
    showTab("python");
}

function copyGuidedToJS(){
    document.getElementById("jsCode").value = document.getElementById("guidedAnswer").value;
    showTab("javascript");
}

function copyGuidedToSQL(){
    document.getElementById("sqlCode").value = document.getElementById("guidedAnswer").value;
    showTab("sql");
}

loadGuidedLessons();


function syncGuidedStepType(){
    if(!currentGuidedLesson) return;
    const step = currentGuidedLesson.steps[currentGuidedStep];
    const selector = document.getElementById("guidedStepType");
    if(selector && step){
        selector.value = step.mode;
    }
}

function jumpGuidedSection(){
    if(!currentGuidedLesson) return;
    const selectedMode = document.getElementById("guidedStepType").value;
    const index = currentGuidedLesson.steps.findIndex(step => step.mode === selectedMode);
    if(index >= 0){
        currentGuidedStep = index;
        renderGuidedStep();
    }
}
