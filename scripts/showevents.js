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

  let new_div = new_element('div', {'class': 'container parent'}, [
    new_element('img', {'src': desc['image']}),

    new_element('div', {'class': 'container parent b'},
    [new_element('div', {'class': 'container parent a'},
    [new_element('h2', {'class': 'tm-text-blue text'}, [document.createTextNode(desc['name'])]),
     new_element('h5', {'class': 'description'}, [document.createTextNode('Performing @ ' + desc['venue'] + ' on ' + desc['date'])])
  ]),
    new_element('div', {'class':'card container xd'},
    [new_element('a', {'href':'/emaillist?event_key_id=' + desc['key'], 'class': 'tm-bg-blue tm-text-white attend'},[document.createTextNode('Attending')]),
    new_element('a', {'class': 'mb-0 desc event_header', 'href': desc['description']}, [document.createTextNode('More Info')]),
    ])
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
