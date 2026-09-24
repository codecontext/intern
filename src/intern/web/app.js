const modelSelect = document.getElementById("model");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send");
const chat = document.getElementById("chat");

let messages = [];


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

        modelSelect.innerHTML = "";

        for (const model of models) {
            const option = document.createElement("option");

            option.value = model;
            option.textContent = model;

            modelSelect.appendChild(option);
        }

    } catch (error) {
        console.error(error);

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

    if (!content || !model) {
        return;
    }


    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    addMessage("user", content);


    messages.push({
        role: "user",
        content: content
    });


    messageInput.value = "";

    resizeInput();


    sendButton.disabled = true;
    modelSelect.disabled = true;
    sendButton.querySelector("span:first-child").textContent = "Thinking...";


    try {

        const response = await fetch(
            `/api/chat?model=${encodeURIComponent(model)}`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(messages)
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


        messages.push({
            role: "assistant",
            content: data.response
        });


    } catch (error) {

        console.error(error);

        addMessage(
            "assistant",
            "Sorry, something went wrong while processing the request."
        );

    } finally {

        sendButton.disabled = false;
        modelSelect.disabled = false;

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


/* ---------------------------------------------------------
   Send button
--------------------------------------------------------- */

sendButton.addEventListener(
    "click",
    sendMessage
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

loadModels();
