/**@type {HTMLDivElement} */
let messagesContainer;
/**@type {HTMLSpanElement} */
let nameSpan;
/**@type {HTMLInputElement} */
let msgInput;
/**@type {HTMLButtonElement} */
let sendMessage;

class Message {
    /**@type {string} */
    name;
    /**@type {string} */
    content;
}


window.addEventListener("load", () => {
    //get elements
    messagesContainer = document.getElementById("messagesContainer");
    nameSpan = document.getElementById("nameSpan");
    msgInput = document.getElementById("msgInput");
    sendMessage = document.getElementById("sendMessage");

    //connect to websocket
    const socket = new WebSocket("/ws");
    //handle messages
    socket.onmessage = (ev) => {
        const data = ev.data;
        console.log(data);
        const msg = JSON.parse(data);
        addMessage(msg)
    };

    //send messages
    sendMessage.addEventListener("click", (ev) => {
        if (ev.button!=0) return;
        socket.send(msgInput.value);
        msgInput.value = "";
    })
});

/**
 * @param {Message}
 */
function addMessage({name, content}) {
    const msgName = document.createElement("span");
    const msgContent = document.createElement("span");
    const msgContainer = document.createElement("p");

    msgName.style.paddingRight = "1em";
    msgName.innerHTML = name;

    msgContent.innerHTML = content;

    msgContainer.append(msgName, msgContent);

    messagesContainer.appendChild(msgContainer);
}