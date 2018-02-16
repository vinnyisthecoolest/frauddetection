const VIEW = 100

const dataColumns = [
  'type', 'amount', 'nameDest', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig'
]

const tableHeaders = [
  'Transaction Type', 'Amount', 'To Account ID',
  'From Account ID', 'Old Balance', 'New Balance'
]

const dataWindow = (data, count) => Object.entries(data)
  .reduce((p, [k, v]) => ({...p, [k]: v.slice(count, VIEW + count)}), {})

const updatePlots = (data) => {
  let count = 0
  const interval = setInterval(() => {
    const newData = dataWindow(data, count)
    const filterArray = newData.prob
      .map((x, i) => x > 0.5 ? {'prob': x, 'pos': i} : false)
    const values = dataColumns
      .map(x => newData[x].filter((x, i) => filterArray[i]))

    const dataUpdate = {y: [newData.prob]}
    const tableUpdate = {
      cells: {
        values: values,
        align: "center",
        line: {color: '#616161', width: 1},
        fill: {color: '#424242'},
        font: {family: "Arial", size: 12, color: 'white'}
      }
    }
    const graphLayout = {
      annotations: filterArray.filter(x => x).map(x => {
        return {
          x: x.pos,
          y: x.prob,
          xref: 'x',
          yref: 'y',
          text: 'FRAUD!',
          showarrow: true,
          arrowhead: 5,
          font: {
            color: '#F44336',
          },
          // ax: 0,
          // ay: -40,
        }
      }),
    }

    Plotly.update('graph', dataUpdate, graphLayout)
    Plotly.update('table', tableUpdate)

    document.getElementById('alert').style.display =
      filterArray[filterArray.length - 1]
      ? 'block'
      : 'none'

    if (count > 999) {
      count = 0
    } else {
      count++
    }
  }, 1000)
}

const tableData = [{
  type: 'table',
  header: {
    values: tableHeaders,
    align: "center",
    line: {width: 1, color: '#616161'},
    fill: {color: 'grey'},
    font: {family: "Arial", size: 14, color: "white"}
  },
  cells: {
    align: "center",
    line: {color: '#616161', width: 1},
    fill: {color: '#424242'},
    font: {family: "Arial", size: 12, color: 'white'}
  }
}]

const tableLayout = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
  margin: {
    t: 0,
    b: 0,
  },
  height: 200,
  autosize: true,
}

const layout = {
  height: 375,
  font: {
    color: 'white',
  },
  autosize: true,
  xaxis: {
    range: [0, 100],
    showgrid: false,
    showline: false,
    zeroline: false,
    fixedrange: true,
    tickmode: 'array',
    tickvals: [0, 50, 100],
    ticktext: ['100', '50', '0'],
    title: 'Time Elapsed',
  },
  yaxis: {
    range: [0, 1],
    showline: false,
    fixedrange: true,
    zeroline: false,
    gridcolor: '#444',
    title: 'Probabilty of Fraud',
  },
  margin: {
    t: 45,
    l: 50,
    r: 50,
    b: 40,
    pad: 5,
  },
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
}

const initialGraphLayout = {
  hoverinfo: 'y'
}

Plotly.d3.json('data.json', (error, data) => {
  if (error) throw error
  const initialData = {y: data.prob.slice(0, 100)}

  Plotly.plot('graph', [{...initialGraphLayout, initialData}], layout, options)
  Plotly.plot('table', tableData, tableLayout, options)

  updatePlots(data)
})

const options = {
  scrollZoom: false,
  showLink: false,
  displayModeBar: false,
}
