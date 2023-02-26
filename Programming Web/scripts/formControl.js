window.addEventListener("load", updateUI());

const questionForm = document.querySelector(".form")
questionForm.addEventListener("submit", (e) => {
    e.preventDefault()
    let input = document.querySelectorAll(".form__input-text")
    const inputData = Object.values(input).map(function (e) {
        return e.value
    })
    if (inputData.includes("")) {
        alert("⛔ Incorrect input!");
        return
    }

    const item = createQuestion(...inputData)
    addQuestion(item)
    questionForm.reset()
});

function getQuestionsList() {
    const questionList = JSON.parse(localStorage.getItem("questionList"))
    return questionList ? questionList : []
};

function addQuestion(item) {
    const questions = getQuestionsList()
    questions.unshift(item)
    updateStorage(questions)
    updateUI()
};

function removeQuestion(item) {
    let questions = getQuestionsList()
    questions = questions.filter(q => JSON.stringify(q) !== JSON.stringify(item))
    updateStorage(questions)
};

function updateStorage(questions) {
    localStorage.setItem("questionList", JSON.stringify(questions))
};

function updateUI() {
    const questions = getQuestionsList()
    const container = document.querySelector(".content-questions__item-list")
    container.innerHTML = ""

    Array.prototype.forEach.call(questions, q => {
        const questionDOM = createQuestionDOM(q.Name, q.Contact, q.Message)
        const questionNode = createHTMLTemplate(questionDOM)
        container.appendChild(questionNode)
    });

    const deleteButtonList = document.querySelectorAll(".item__delete-button")
    deleteButtonList.forEach((b, index) => {
        b.addEventListener("click", () => {
            removeQuestion(questions[index])
            updateUI()
        })
    })
};

function createQuestion(name, contact, message) {
    return {
        Name: name,
        Contact: contact,
        Message: message
    }
};

function createQuestionDOM(name, contact, message) {
    return `
        <div class="content-questions__item item">
            <div class="item__body">
                <button class="item__delete-button">✖</button>
                <div class="item__name">Name: ${name}</div>
                <div class="item__contact-info">Contact: ${contact}</div>
                <div class="item__text">Message: ${message}</div>
            </div>
        </div>`
};

function createHTMLTemplate(stringContent) {
    let template = document.createElement('template');
    stringContent = stringContent.trim();
    template.innerHTML = stringContent
    return template.content.firstChild;
};