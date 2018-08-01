function new_element(tag_name, attributes, children=[]){
  let el = document.createElement(tag_name)
  for (let attr in attributes){
    el.setAttribute(attr, attributes[attr]);
  }
  for (let child in children){
    el.appendChild(children[child]);
  }
  return el
}

function insert_events(desc){

  let new_div = new_element('div', {'class': 'event'}, [
    new_element('img', {'src': desc['image']}),

    new_element('div', {'class': 'event-body tm-bg-gray'},
    [new_element('div', {'class': 'tm-description-box'},
    [new_element('h5', {'class': 'tm-text-blue'}, [document.createTextNode(desc['artist'])]),
    new_element('p', {'class': 'mb-0'}, [document.createTextNode(desc['description'])])]),
    new_element('div', {'class':'tm-buy-box'},
    [new_element('a', {'href':'/emaillist?event_key_id=' + desc['key'], 'class': 'tm-bg-blue tm-text-white tm-buy'},[document.createTextNode('Attending')]),
    new_element('span', {'class': 'tm-text-blue tm-price-tag'}, [document.createTextNode(desc['date'])])])
  ])
    // new_element('div', {'src': 'meme_templates/' + desc['image_file']}),
    // new_element('h2', {'class': 'line1'}, [document.createTextNode(desc['top_text'])]),
    // new_element('h2', {'class': 'line2'}, [document.createTextNode(desc['bottom_text'])]),
  ]);
  let container = document.querySelector("#displayevents");
  console.log(container)
  console.log(container.children)
  container.insertBefore(new_div, null );
  // container.children[((container.children).length -1)]

}




function show_events(){
  fetch('/eventlist', {'credentials': 'include'})
  .then((data) => {return data.json()})
  .then((json) => {
    for (let i in json){
      insert_events(json[i]);
    }

  })
}

// function refresh_memes() {
//   fetch('/updated_memes?since=' + last_refresh.getTime()/1000, {'credentials': 'include'} )
//     .then((data) => {return data.json()})
//     .then((json) => {
//       for (let i in json) {
//         insert_meme(json[i]);
//       }
//     })
//   last_refresh = new Date();
// }
//

show_events()
