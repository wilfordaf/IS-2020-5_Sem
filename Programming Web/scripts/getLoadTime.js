(() => {
    const startTime = Date.now()
    window.addEventListener("load", () => {
        const endTime = Date.now()
        const el = document.querySelector(".header-loadtime__text")
        el.innerText = `Total load time: ${endTime - startTime} ms (client) + {} ms (server)`
    })
})()