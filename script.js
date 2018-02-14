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
    // const filterArray = newData.prob.map(x => x > 0.5 ? true : false)
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
            // family: 'Courier New, monospace',
            // size: 14,
            color: '#F44336',
          },
          ax: 0,
          ay: -40,
        }
      })
    }

    Plotly.update('graph', dataUpdate, graphLayout)
    Plotly.update('table', tableUpdate)

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
    // values: [],
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
    t: 20
  },
  height: 250,
}

const layout = {
  height: 450,
  xaxis: {
    range: [0, 100],
    showgrid: false,
    showline: false,
    zeroline: false,
    fixedrange: true,
    // tickvals=[0, 50, 100, 150, 200],
    // ticktext=['200', '150', '100', '50', '0'],
    title: 'Time',
  },
  yaxis: {
    range: [0, 1],
    showline: false,
    fixedrange: true,
    zeroline: false,
    title: 'Probabilty of Fraud',
  },
  margin: {
    t: 45,
    l: 50,
    r: 50,
  },
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)'
  // paper_bgcolor: '#424242',
  // plot_bgcolor: '#424242'
  // annotations: []
}

Plotly.d3.json('data.json', (error, data) => {
  if (error) throw error

  // const tableValues = dataColumns.map(x => data[x].slice(0, 100))

  Plotly.plot('graph', [{y: data.prob.slice(0, 100)}], layout, options)
  Plotly.plot('table', tableData, tableLayout, options)

  updatePlots(data)
})

const options = {
  scrollZoom: false, // lets us scroll to zoom in and out - works
  showLink: false, // removes the link to edit on plotly - works
  // modeBarButtonsToRemove: ['toImage', 'zoom2d', 'pan', 'pan2d', 'autoScale2d'],
  //modeBarButtonsToAdd: ['lasso2d'],
  displayLogo: false, // this one also seems to not work
  displayModeBar: false, //this one does work
}
