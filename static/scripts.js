document.addEventListener("DOMContentLoaded", () => {
  console.log("Javascript Loaded")

  // TEST

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
  }

  var ctx = document.getElementById('myChart')
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: times.map(x=>moment(x[0], "YYYY/MM/DD").format("ddd MMM D")),
        datasets: [{
          label: "Individual Sleep Times",
          borderColor: 'rgba(153, 44, 127, 0.5)',
          backgroundColor: 'rgba(153, 44, 127, 0.5)',
          data: times.map(x=>x[3])
        },{
          label: "Sleep Times Smooth",
          data: times.map(x=>x[3]),
          type: "line",
          borderColor: 'rgba(153, 44, 127)',
          backgroundColor: 'rgba(153, 44, 127)',
          fill: false,
          radius: 0
        },{
          label: "Day energy",
          data: times.map(x=>x[5]),
          type: "bar",
          borderColor: 'rgba(34, 141, 204, 0.5)',
          backgroundColor: 'rgba(34, 141, 204, 0.5)',
          fill: false,
        },{
          label: "5-Day Sleep Trend",
          data: times.map(x=>x[6]),
          type: "line",
          borderColor: 'rgba(219, 116, 26)',
          backgroundColor: 'rgba(219, 116, 26)',
          fill: false,
        }]
    },
    options: {
      tooltips: {
        callbacks: {
          label: function(item, data) {

            let label = data.datasets[item.datasetIndex].label
            if (label == "5-Day Sleep Trend" || label == "Day energy"){
              let trend = moment.duration(parseInt(item.value), "minutes")
              console.log(trend)
              let hours = parseInt(trend.asHours())
              console.log(hours)
              let minutes = trend.asMinutes() - hours * 60

              return `${hours} hours ${minutes} minutes.`
            }
            else if (label == "Individual Sleep Times"){
              let time = times[item["index"]]
              let sleep_time = moment(time[1], "YYYY/MM/DD HH:mm:ss").format("h:mm a")
              let wake_time = moment(time[2], "YYYY/MM/DD HH:mm:ss").format("h:mm a")
              return [
                "Sleep: " + sleep_time,
                "Wake: " + wake_time,
                "Rested: " + time[4]
              ]
            }
          }
        }
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
            stepSize: 60,
            callback: x => {
              hours = moment.duration(x, "minutes").asHours()
              if (hours == 1) {
                return hours + " hour"
              }
              else {
                return hours + " hours"
              }
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
