mermaid.initialize({
  startOnLoad: true,
})

var showInfo = (x) => {
  for (let info of document.getElementsByClassName('info')) {
    info.classList.remove('active')
  }
  document.getElementById(x + '-info').classList.add('active')
}

document.getElementById('button').onclick = () => showInfo('default')
