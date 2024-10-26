function onWindowLoad() {
    var message = document.querySelector('#message');
    var title = document.querySelector('#title');

    chrome.tabs.query({ active: true, currentWindow: true }).then(function (tabs) {
        var activeTab = tabs[0];
        var activeTabId = activeTab.id;

        return chrome.scripting.executeScript({
            target: { tabId: activeTabId },
            func: DOMtoString,
            });

    }).then(function (results) {
        var html = results[0].result;
        var parser = new DOMParser()
        var doc = parser.parseFromString(html, "text/html")
        if (doc.querySelector("meta[property='og:title']").getAttribute("content") == "ChatGPT") {
            var convo = []
            var i = 2
            while (doc.querySelector('article[data-testid="conversation-turn-' + i + '"]') != undefined) {
                convo.push(doc.querySelector('article[data-testid="conversation-turn-' + i + '"]'))
                ++i
            }
            var lastResponse = convo[convo.length - 1]
            message.innerText = lastResponse.getElementsByClassName("markdown")[0].textContent
        } else if (doc.querySelector("title").textContent.search("Claude") != -1) {
            message.innerText = doc.querySelector('div[data-test-render-count="1"]').getElementsByClassName("font-claude-message")[0].textContent
        } else if (doc.querySelector("meta[property='og:site_name']").getAttribute("content") == "Gemini") {
            var responses = doc.querySelectorAll("message-content")
            message.innerText = responses[responses.length - 1].textContent
        } else {
            throw new Error("")
        }
    }).catch(function (error) {
        const textInput = document.createElement("input")
        const button = document.createElement("button")
        button.textContent = "Submit"
        button.addEventListener('click', ()=> {
            message.innerHTML = textInput.value
            document.body.removeChild(textInput)
            document.body.removeChild(button)
        })
        document.body.appendChild(textInput)
        document.body.appendChild(button)
        title.innerText = 'No prompt from Claude, Gemini, or ChatGPT detected. Please enter the information you want to fact check.';
    });
}

window.onload = onWindowLoad;

function DOMtoString(selector) {
    if (selector) {
        selector = document.querySelector(selector);
        if (!selector) return "ERROR: querySelector failed to find node"
    } else {
        selector = document.documentElement;
    }
    return selector.outerHTML;
}