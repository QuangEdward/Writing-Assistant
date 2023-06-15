let getValue = document.querySelector('.value').value
let getNumberValue = Math.round(Number(getValue))
let progressCircular = document.querySelector('.progress-circular')
let start = 0
function bar() {
    let progress = setInterval(() => {
        if (start < getNumberValue) {
            start++
            progressEnd()
        }
        else {
            start--
            progressEnd()
        }
        function progressEnd() {
            progressCircular.style.background = `conic-gradient(blueviolet ${start * 3.6}deg, #ccc 0deg) !important`
            if (start == getNumberValue) {
                clearInterval(progress)
            }
        }
    }, 30)
}
bar()