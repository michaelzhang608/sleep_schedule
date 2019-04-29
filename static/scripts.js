document.addEventListener("DOMContentLoaded", () => {
  console.log("Javascript Loaded")


  // Get times
  let times_html = $("#times").children()
  let display = $("#info_display")
  let times = []
  for (let i = 0; i < times_html.length; i++) {

    let time_items = $(times_html[i]).children()
    let temp = []
    for (let i2 = 0; i2 < time_items.length; i2++) {

      temp.push(time_items[i2].innerHTML)
    }
    times.push(temp)

    let div = document.createElement("div")
    div.innerHTML = temp[0] + ": "+ temp[4]
    // info_display.append(div)
    // info_display.append(document.createElement("br"))
  }

  var ctx = document.getElementById('myChart')
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: times.map(x=>moment(x[0], "YYYY/MM/DD").format("ddd MMM D")),
        datasets: [{
          label: "Individual Sleep Times",
          data: times.map(x=>x[3])
        },{
          label: "Sleep Times Trend",
          data: times.map(x=>x[3]),
          type: "line",
          borderColor: 'rgba(153, 44, 127)',
          backgroundColor: 'rgba(153, 44, 127)',
          pointBackgroundColor: 'rgba(0, 0, 0, 0)',
          pointBorderColor: 'rgba(0, 0, 0, 0)',
          fill: false
        }]
    },
    options: {
      tooltips: {
        callbacks: {
          label: function(x) {
            return moment.duration(parseInt(x["value"]), "minutes").humanize()
          }
        }
      },
      scales: {
        xAxes: [{
          ticks: {
            // callback: x => {
            //   return moment(x, "dddd MMM D").format("MMM D")
            // }
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            callback: x => {
              return moment.duration(x, "minutes").humanize()
            }
          }
        }]
      }
    }
  })

  // Fade out all divs and fade in specific div
  function change_to(div) {
    let all_children = document.querySelector("#main").children
    for (let i = 0; i < all_children.length; i++) {
      $(all_children[i]).fadeOut()
    }

    setTimeout(() => {
      $(div).fadeIn()
    }, 400)
    return false
  }
})
