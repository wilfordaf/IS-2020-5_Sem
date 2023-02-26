const PAGE_SIZE = 5
const errorBlock = document.querySelector(".content-qna__error")
const qnaList = document.querySelector(".content-qna__item-list")
const panel = document.querySelector(".panel")
const preloader = document.querySelector(".content-qna__preloader")
let CURRENT_PAGE = 1

window.addEventListener("load", getQnA(CURRENT_PAGE))

async function getQnA() {
    qnaList.style.display = "none"
    errorBlock.style.display = "none"
    preloader.style.display = "block"
    
    const SLICE_SIZE = 100
    const questionLink = "https://jsonplaceholder.typicode.com/comments"
    await fetch(questionLink)
        .then((data) => data.json())
        .then((data) => {
            if (!(doesCurrentPageExist(SLICE_SIZE))) {
                CURRENT_PAGE = 1
                throw RangeError("Page number is invalid")
            }

            const randomSlice = Math.floor(Math.random() * 5 + 1)
            const dataSliced = data.slice((randomSlice - 1) * SLICE_SIZE, randomSlice * SLICE_SIZE)
            
            updatePaginationPanel(Math.ceil(SLICE_SIZE / PAGE_SIZE))
            const pageContent = dataSliced.slice((CURRENT_PAGE - 1) * PAGE_SIZE, CURRENT_PAGE * PAGE_SIZE)
            pageContent.forEach(element => {
                const qnaDOM = createQnADOM(element)
                const qnaTemplate = createHTMLTemplate(qnaDOM)
                qnaList.appendChild(qnaTemplate)
            });

            preloader.style.display = "none"
            qnaList.style.display = "block"
        })
        .catch((error) => {
            errorBlock.innerHTML = ""
            errorBlock.innerHTML += `⚠️ Something went wrong!<br>"${error.message}"`
            preloader.style.display = "none"
            qnaList.style.display = "none"
            errorBlock.style.display = "block"
        })
};

function createQnADOM(element) {
    const messageSplit = element.body.split("\n")
    const question = messageSplit.slice(0, -1).join(" ")
    const answer = messageSplit[messageSplit.length - 1]
    return `
        <div class="content-qna__item item">
            <div class="item__body">
                <div class="item__name">Name: ${element.name}</div>
                <div class="item__contact-info">Contact: ${element.email}</div>
                <div class="item__text">Question: ${question}?</div>
                <div class="item__text">Answer: ${answer}.</div>
            </div>
        </div>`
};

function createPaginationPanelDOM(pagesCount) {
    let content = `<div class="panel__body">`
    content += `<li><button class="panel__button button-prev">◂</button></li>`
    if (CURRENT_PAGE > 1) {
        content += `<li><button class="panel__button button-page">1</button></li>`
    }

    if (CURRENT_PAGE > 3) {
        content += `<li>...</li>`
    }

    if (CURRENT_PAGE > 2) {
        content += `<li><button class="panel__button button-page">${CURRENT_PAGE - 1}</button></li>`
    }

    content += `<li><button class="panel__button button-page">${CURRENT_PAGE}</button></li>`
    if (CURRENT_PAGE < pagesCount - 1) {
        content += `<li><button class="panel__button button-page">${CURRENT_PAGE + 1}</button></li>`
    }

    if (CURRENT_PAGE < pagesCount - 2) {
        content += "<li>...</li>"
    }

    if (CURRENT_PAGE < pagesCount) {
        content += `<li><button class="panel__button button-page">${pagesCount}</button></li>`
    }

    content += `<li><button class="panel__button button-next">▸</button></li></div>`
    return content
};

function doesCurrentPageExist(dataLength) {
    return CURRENT_PAGE > 0 && CURRENT_PAGE * PAGE_SIZE <= dataLength + dataLength % PAGE_SIZE
};

function updatePaginationPanel(pagesCount) {
    qnaList.replaceChildren()
    const panelBodyDOM = createPaginationPanelDOM(pagesCount)
    const panelBodyTemplate = createHTMLTemplate(panelBodyDOM)

    panel.replaceChildren()
    panel.appendChild(panelBodyTemplate)

    const buttons = panel.querySelectorAll(".panel__body li button")
    buttons.forEach(b => {
        if (b.innerText == CURRENT_PAGE) {
            b.classList.add("active-page")
            return
        }
    })

    buttonActionHandler()
};

function buttonActionHandler() {
    const buttonNext = document.querySelector(".button-next")
    buttonNext.addEventListener("click", () => {
        CURRENT_PAGE++
        getQnA(CURRENT_PAGE)
    })

    const buttonPrev = document.querySelector(".button-prev")
    buttonPrev.addEventListener("click", () => {
        CURRENT_PAGE--
        getQnA(CURRENT_PAGE)
    })

    const pageButtons = document.querySelectorAll(".button-page")
    pageButtons.forEach(b => {
        b.addEventListener("click", () => {
            CURRENT_PAGE = parseInt(b.innerText, 10)
            getQnA(CURRENT_PAGE)
        })
    })
};