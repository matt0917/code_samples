/* 
Author : Joonseo Park
*/

// default localStorage sanitary
const clear_local_data = () => {
  localStorage.clear();
};

local_data_key_map = {
  image: "image_data",
};

// fetchning data
let images = JSON.parse(localStorage.getItem(local_data_key_map.image));
let num_to_win;
// factors: -12, -7, 0, 9, 20, 33
var game_level_factor = 0;

const fetch_data = new Promise((resolve, error) => {
  let url = "data/fruits.json";
  if (!images) {
    fetch(url)
      .then((response) => response.json())
      .then((json) => {
        images = json;
        if (!Array.isArray(json)) {
          images = [json];
        }
        localStorage.setItem(local_data_key_map.image, JSON.stringify(images));
        num_to_win = images.length + game_level_factor;
        resolve([images, num_to_win]);
      })
      .catch(() => {
        error("No data found");
      });
  } else {
    num_to_win = images.length + game_level_factor;
    resolve([images, num_to_win]);
  }
});

// initiate fruits
let grid_num = Math.pow(num_to_win, 0.5);
let paired_number;
let keys_count;
let keys;
fetch_data
  .then(([images, num_to_win]) => {
    paired_number = num_to_win / 2;
    // check data
    if (!check_paired(images, paired_number)) {
      console.log(
        `Invalid a number of pairs of fruits: ${keys_count} differs from ${paired_number}. Aborted`
      );
      return;
    } else {
      console.log(`Fruits: ${keys}`);
      console.log(`Fruit count: ${keys_count}, Paired`);
    }
    let game = document.getElementById("game");
    // set game layout
    set_game(game);
    // shuffle images
    images.slice(0, num_to_win).sort();
    console.log(images);
    images = shuffle_array(images);
    // add images
    add_images(game);
  })
  .catch((msg) => {
    console.log(msg);
  });

function init() {
  fetch_data;
}

// init
window.addEventListener("load", init);

// check if the images have the right number of pairs of fruits
const check_paired = (images, paired_number) => {
  let pairObj = {};
  for (let i = 0; i < images.length; i++) {
    let basename = images[i].split("-").slice(-1)[0];
    let fruit = basename.split(".")[0];
    if (!pairObj.hasOwnProperty(fruit)) {
      pairObj[fruit] = 1;
    } else {
      pairObj[fruit] += 1;
    }
  }
  keys = Object.keys(pairObj);
  keys_count = Object.keys(pairObj).length;
  let count_status = keys_count === paired_number;
  let paired_status = true;
  for (key of keys) {
    if (pairObj[key] !== 2) {
      paired_status = false;
      break;
    }
  }
  return true;
  return count_status && paired_status;
};

// set game layout
const set_game = (game) => {
  game.style.gridTemplateColumns = `repeat(${grid_num}, 128px)`;
  game.style.gridTemplateRows = `repeat(${grid_num}, 128px)`;
};

// shuffle images using Fisher-Yates shuffle algorithm
const shuffle_array = (array) => {
  let curIdx = array.length;
  // There remain items to shuffle
  while (0 !== curIdx) {
    let randIdx = Math.floor(Math.random() * curIdx);
    curIdx -= 1; // keep reducing by 1 until curIdx becomes 1
    // swap the radom index with the current item with random Idx
    let tmp = array[curIdx];
    array[curIdx] = array[randIdx];
    array[randIdx] = tmp;
  }
  return array;
};

// add images to card img element
const add_images = (game) => {
  // create div img elements for the number of the array data
  for (let i = 1; i <= num_to_win; i++) {
    let cardName = `card${i}`;
    let card = document.createElement("div");
    card.classList.add("card");
    let img = document.createElement("img");
    img.setAttribute("alt", cardName);
    card.appendChild(img);
    game.appendChild(card);
  }

  // define images pathes
  const cards = document.querySelectorAll("div.card img");
  let i = 0;
  cards.forEach((card) => {
    // console.log(images[i]);
    card.setAttribute("src", images[i]);
    i++;
  });
};

// Game logic part
// vars
let max_revealed = 2;
let found = "found";
let revealed = "revealed";
let disabled = "disabled";

class RevealedCard {
  constructor() {
    this.cards = Array.from(document.querySelectorAll(`img.${revealed}`));
    this.num = this.cards.length;
  }
}

const num_found = () => {
  return Array.from(document.querySelectorAll(`img.${found}`)).length;
};

// check if the current state is valid to reveal another card
const tag_cards = () => {
  // check currently revealed cards by creating new object
  let revealedObj = new RevealedCard();
  if (revealedObj.num === max_revealed) {
    let cardA = revealedObj.cards[0];
    let cardB = revealedObj.cards[1];
    if (cardA.getAttribute("src") === cardB.getAttribute("src")) {
      // console.log(cardA, cardB)
      // add found class
      cardA.classList.add(found);
      cardB.classList.add(found);
      // remove revealed class
      cardA.classList.remove(revealed);
      cardB.classList.remove(revealed);
      // add disabled class
      cardA.classList.add(disabled);
      cardB.classList.add(disabled);
      // if found == num_to_win, set win and end of the current game
      if (num_found() == num_to_win) {
        set_win();
      }
    }
  }
};

// add listeners to clicked element
document.addEventListener("click", (event) => {
  let el = event.target;
  let parent = el.parentNode;

  // element has card class
  if (parent.classList.contains("card")) {
    // check currently revealed cards
    let revealedObj = new RevealedCard();
    // console.log(revealedObj.cards)
    // console.log(revealedObj.num)
    // if the card does not have revealed and found classes and less than 2 cards currently revealed add the class revealed
    // Otherwise, remove revealed class from the card element
    if (!el.classList.contains(revealed) && !el.classList.contains(found)) {
      if (revealedObj.num < max_revealed) {
        el.classList.add(revealed);
        tag_cards();
      }
    } else {
      el.classList.remove(revealed);
    }
  }
});

const set_win = () => {
  document.body.classList.add("win");
};
