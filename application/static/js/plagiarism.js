let getValue = document.querySelector('.value').textContent
let getNumberValue = Math.round(Number(getValue))
let progressCircular = document.querySelector('.progress-circular')
console.log(progressCircular)
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
            progressCircular.style.background = `conic-gradient(#F34444 ${start * 3.6}deg, #fff 0deg)`
            if (start == getNumberValue) {
                clearInterval(progress)
            }
        }
    }, 30)
    
}
bar()