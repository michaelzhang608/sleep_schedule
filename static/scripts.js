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
    info_display.append(div)
    info_display.append(document.createElement("br"))
  }


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

  // TODO

})
