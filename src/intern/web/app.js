const modelSelect = document.getElementById("model");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send");
const chat = document.getElementById("chat");
const knowledgeBaseForm = document.getElementById("knowledge-base-form");
const knowledgeBasePath = document.getElementById("knowledge-base-path");
const knowledgeBaseAdd = document.getElementById("knowledge-base-add");
const knowledgeBaseToggle = document.getElementById("knowledge-base-toggle");
const knowledgeBaseToggleLabel = document.getElementById("knowledge-base-toggle-label");
const knowledgeBasePanel = document.getElementById("knowledge-base-panel");
const knowledgeBaseSourcesLabel = document.getElementById("knowledge-base-sources-label");
const knowledgeBaseSources = document.getElementById("knowledge-base-sources");
const knowledgeBaseStatus = document.getElementById("knowledge-base-status");

let conversationId = null;
let loadedKnowledgeBasePaths = [];


/* ---------------------------------------------------------
   Knowledge bases
--------------------------------------------------------- */

function pluralizeCount(count, singular, plural = `${singular}s`) {
    return `${count} ${count === 1 ? singular : plural}`;
}


function formatKnowledgeBaseStatus(sourceCount, documentCount) {
    return `${pluralizeCount(sourceCount, "source")} · ${pluralizeCount(documentCount, "document")}`;
}

function renderKnowledgeBases(knowledgeBases) {
    if (knowledgeBases.length === 0) {
        knowledgeBaseStatus.textContent = "No knowledge source loaded";
        loadedKnowledgeBasePaths = [];
        renderSourcePaths([]);
        return;
    }

    loadedKnowledgeBasePaths = knowledgeBases.flatMap(
        (knowledgeBase) => knowledgeBase.source_paths
    );
    renderSourcePaths(loadedKnowledgeBasePaths);

    knowledgeBaseStatus.textContent = knowledgeBases
        .map((knowledgeBase) => {
            return formatKnowledgeBaseStatus(
                knowledgeBase.source_paths.length,
                knowledgeBase.document_count,
            );
        })
        .join(" | ");
}


function renderSourcePaths(sourcePaths) {
    const hasSources = sourcePaths.length > 0;

    knowledgeBaseSourcesLabel.hidden = !hasSources;
    knowledgeBaseSources.hidden = !hasSources;
    knowledgeBaseSources.innerHTML = "";

    for (const sourcePath of sourcePaths) {
        const source = document.createElement("div");
        const label = document.createElement("span");

        source.className = "knowledge-base-source";
        label.textContent = sourcePath;
        source.append(label);

        knowledgeBaseSources.appendChild(source);
    }
}


function showKnowledgeBaseError(message) {
    const prefix = "Source path does not exist:";

    knowledgeBaseStatus.replaceChildren();
    knowledgeBaseStatus.classList.add("error");

    if (message.startsWith(prefix)) {
        const errorPrefix = document.createElement("span");
        const errorPath = document.createElement("span");

        errorPrefix.textContent = `${prefix} `;
        errorPath.className = "knowledge-base-error-path";
        errorPath.textContent = message.slice(prefix.length).trim();
        knowledgeBaseStatus.append(errorPrefix, errorPath);
        return;
    }

    knowledgeBaseStatus.textContent = message;
}


async function addKnowledgeBasePath() {
    const sourcePath = knowledgeBasePath.value.trim();

    if (!sourcePath || loadedKnowledgeBasePaths.includes(sourcePath)) {
        return;
    }

    knowledgeBaseAdd.classList.remove("is-clicked");
    void knowledgeBaseAdd.offsetWidth;
    knowledgeBaseAdd.classList.add("is-clicked");
    knowledgeBaseAdd.disabled = true;
    knowledgeBaseStatus.classList.remove("error");
    knowledgeBaseStatus.textContent = "Checking path...";

    try {
        const response = await fetch("/api/knowledge-bases/validate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                source_paths: [sourcePath]
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "The path could not be read");
        }

        const sourcePaths = [...loadedKnowledgeBasePaths, sourcePath];
        const loadResponse = await fetch("/api/knowledge-bases", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                source_paths: sourcePaths
            })
        });

        if (!loadResponse.ok) {
            const error = await loadResponse.json();
            throw new Error(error.detail || "Failed to add knowledge source");
        }

        const knowledgeBase = await loadResponse.json();
        loadedKnowledgeBasePaths = knowledgeBase.source_paths;
        renderSourcePaths(loadedKnowledgeBasePaths);
        knowledgeBasePath.value = "";
        knowledgeBaseStatus.classList.remove("error");
        knowledgeBaseStatus.textContent = `${formatKnowledgeBaseStatus(
            loadedKnowledgeBasePaths.length,
            knowledgeBase.document_count,
        )} added`;
    } catch (error) {
        console.error(error);
        showKnowledgeBaseError(error.message);
    } finally {
        knowledgeBaseAdd.disabled = false;
        window.setTimeout(() => {
            knowledgeBaseAdd.classList.remove("is-clicked");
        }, 450);
        knowledgeBasePath.focus();
    }
}


function updateKnowledgeBaseButton() {
    knowledgeBaseAdd.classList.toggle(
        "path-ready",
        knowledgeBasePath.value.trim().length > 0
    );
}


async function addKnowledgeBase(event) {
    event.preventDefault();
    await addKnowledgeBasePath();
}


function toggleKnowledgeBasePanel() {
    knowledgeBasePanel.hidden = !knowledgeBaseToggle.checked;
    knowledgeBaseToggleLabel.textContent = knowledgeBaseToggle.checked
        ? "ON"
        : "OFF";
}


/* ---------------------------------------------------------
   Create backend conversation
--------------------------------------------------------- */

async function createConversation() {
    const response = await fetch("/api/conversations", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to create conversation");
    }

    const data = await response.json();
    conversationId = data.conversation_id;
}


/* ---------------------------------------------------------
   Load available Ollama models
--------------------------------------------------------- */

async function loadModels() {
    try {
        const response = await fetch("/api/models");

        if (!response.ok) {
            throw new Error("Failed to load models");
        }

        const models = await response.json();

        if (models.length === 0) {
            throw new Error("No models available");
        }

        modelSelect.innerHTML = "";

        for (const model of models) {
            const option = document.createElement("option");

            option.value = model;
            option.textContent = model;

            modelSelect.appendChild(option);
        }

        modelSelect.disabled = false;
        messageInput.disabled = false;
        sendButton.disabled = false;

    } catch (error) {
        console.error(error);

        modelSelect.disabled = true;
        messageInput.disabled = true;
        sendButton.disabled = true;

        modelSelect.innerHTML = `
            <option value="">Unable to load models</option>
        `;
    }
}


/* ---------------------------------------------------------
   Add message to chat
--------------------------------------------------------- */

function escapeHtml(content) {
    return content
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function formatInlineMarkdown(content) {
    return content
        .replace(/`([^`\n]+)`/g, "<code>$1</code>")
        .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>")
        .replace(/__([^_\n]+)__/g, "<strong>$1</strong>")
        .replace(/\*([^*\n]+)\*/g, "<em>$1</em>")
        .replace(/_([^_\n]+)_/g, "<em>$1</em>");
}


function formatMarkdown(content) {
    const lines = escapeHtml(content).split("\n");
    const formattedLines = [];
    let inList = false;

    for (const line of lines) {
        const listItem = line.match(/^\s*[-*]\s+(.+)$/);

        if (listItem) {
            if (!inList) {
                formattedLines.push("<ul>");
                inList = true;
            }

            formattedLines.push(
                `<li>${formatInlineMarkdown(listItem[1])}</li>`
            );
            continue;
        }

        if (inList) {
            formattedLines.push("</ul>");
            inList = false;
        }

        formattedLines.push(formatInlineMarkdown(line));
    }

    if (inList) {
        formattedLines.push("</ul>");
    }

    return formattedLines.join("<br>");
}

function addMessage(role, content) {
    const message = document.createElement("div");
    const messageContent = document.createElement("div");
    const timestamp = document.createElement("span");

    message.classList.add("message");
    message.classList.add(role);

    messageContent.classList.add("message-content");
    messageContent.innerHTML = formatMarkdown(content);

    timestamp.classList.add("message-time");
    timestamp.textContent = new Intl.DateTimeFormat([], {
        hour: "numeric",
        minute: "2-digit"
    }).format(new Date());

    message.appendChild(messageContent);
    message.appendChild(timestamp);

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


/* ---------------------------------------------------------
   Send message
--------------------------------------------------------- */

async function sendMessage() {

    const content = messageInput.value.trim();
    const model = modelSelect.value;

    if (!content || !model || !conversationId) {
        return;
    }


    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    addMessage("user", content);


    messageInput.value = "";

    resizeInput();


    sendButton.disabled = true;
    modelSelect.disabled = true;
    sendButton.classList.add("is-busy");
    sendButton.querySelector("span:first-child").textContent = "Thinking...";


    try {

        const response = await fetch(
            `/api/conversations/${encodeURIComponent(conversationId)}/messages`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    model: model,
                    message: content
                })
            }
        );


        if (!response.ok) {
            throw new Error("Chat request failed");
        }


        const data = await response.json();


        addMessage(
            "assistant",
            data.response
        );


    } catch (error) {

        console.error(error);

        addMessage(
            "assistant",
            "Sorry, something went wrong while processing the request."
        );

    } finally {

        sendButton.disabled = false;
        modelSelect.disabled = false;
        sendButton.classList.remove("is-busy");

        sendButton.querySelector("span:first-child").textContent = "Send";

        messageInput.focus();
    }
}


/* ---------------------------------------------------------
   Auto resize input
--------------------------------------------------------- */

function resizeInput() {

    messageInput.style.height = "auto";

    messageInput.style.height =
        Math.min(messageInput.scrollHeight, 160) + "px";
}


messageInput.addEventListener(
    "input",
    resizeInput
);


knowledgeBasePath.addEventListener(
    "input",
    updateKnowledgeBaseButton
);


/* ---------------------------------------------------------
   Send button
--------------------------------------------------------- */

sendButton.addEventListener(
    "click",
    sendMessage
);


knowledgeBaseForm.addEventListener(
    "submit",
    addKnowledgeBase
);


knowledgeBaseToggle.addEventListener(
    "change",
    toggleKnowledgeBasePanel
);


/* ---------------------------------------------------------
   Keyboard handling
--------------------------------------------------------- */

messageInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();

            sendMessage();
        }

    }
);


/* ---------------------------------------------------------
   Startup
--------------------------------------------------------- */

Promise.all([
    loadModels(),
    createConversation(),
    fetch("/api/knowledge-bases")
        .then((response) => response.json())
        .then(renderKnowledgeBases)
]).catch((error) => {
    console.error(error);
    addMessage(
        "assistant",
        "Sorry, a conversation could not be started."
    );
});


updateKnowledgeBaseButton();
