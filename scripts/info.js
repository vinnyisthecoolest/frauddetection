mermaid.initialize({
  startOnLoad: true,
})

var showInfo = (x) => {
  for (let info of document.getElementsByClassName('info')) {
    info.classList.remove('active')
  }

  for (let node of document.getElementsByClassName('node')) {
    node.classList.remove('active-node')
  }

  document.getElementById(x + '-info').classList.add('active')
  document.getElementById(x).classList.add('active-node')
}

document.getElementById('default').onclick = () => showInfo('default')
