// Movie Recommender - browser version.
// Same method as recommend.py: TF-IDF over each movie's genres + keywords,
// then cosine similarity between movies. No server, no install.

// English stop words, the same list scikit-learn's TfidfVectorizer uses.
const STOP_WORDS = new Set(("a,about,above,across,after,afterwards,again,against,all,almost,alone,along,already,also,although,always,am,among,amongst,amoungst,amount,an,and,another,any,anyhow,anyone,anything,anyway,anywhere,are,around,as,at,back,be,became,because,become,becomes,becoming,been,before,beforehand,behind,being,below,beside,besides,between,beyond,bill,both,bottom,but,by,call,can,cannot,cant,co,con,could,couldnt,cry,de,describe,detail,do,done,down,due,during,each,eg,eight,either,eleven,else,elsewhere,empty,enough,etc,even,ever,every,everyone,everything,everywhere,except,few,fifteen,fifty,fill,find,fire,first,five,for,former,formerly,forty,found,four,from,front,full,further,get,give,go,had,has,hasnt,have,he,hence,her,here,hereafter,hereby,herein,hereupon,hers,herself,him,himself,his,how,however,hundred,i,ie,if,in,inc,indeed,interest,into,is,it,its,itself,keep,last,latter,latterly,least,less,ltd,made,many,may,me,meanwhile,might,mill,mine,more,moreover,most,mostly,move,much,must,my,myself,name,namely,neither,never,nevertheless,next,nine,no,nobody,none,noone,nor,not,nothing,now,nowhere,of,off,often,on,once,one,only,onto,or,other,others,otherwise,our,ours,ourselves,out,over,own,part,per,perhaps,please,put,rather,re,same,see,seem,seemed,seeming,seems,serious,several,she,should,show,side,since,sincere,six,sixty,so,some,somehow,someone,something,sometime,sometimes,somewhere,still,such,system,take,ten,than,that,the,their,them,themselves,then,thence,there,thereafter,thereby,therefore,therein,thereupon,these,they,thick,thin,third,this,those,though,three,through,throughout,thru,thus,to,together,too,top,toward,towards,twelve,twenty,two,un,under,until,up,upon,us,very,via,was,we,well,were,what,whatever,when,whence,whenever,where,whereafter,whereas,whereby,wherein,whereupon,wherever,whether,which,while,whither,who,whoever,whole,whom,whose,why,will,with,within,without,would,yet,you,your,yours,yourself,yourselves").split(","));

// Split text into words of 2+ letters/numbers, like scikit-learn does.
function tokenize(text) {
  const words = text.toLowerCase().match(/[a-z0-9_]{2,}/g) || [];
  return words.filter((word) => !STOP_WORDS.has(word));
}

// Build one TF-IDF vector (as a Map of word -> weight) per movie.
function buildVectors(movies) {
  const docs = movies.map((movie) => tokenize(movie.genres + " " + movie.keywords));

  // Document frequency: in how many movies does each word appear?
  const docFreq = new Map();
  for (const doc of docs) {
    for (const word of new Set(doc)) {
      docFreq.set(word, (docFreq.get(word) || 0) + 1);
    }
  }

  // scikit-learn's idf formula: ln((1 + n) / (1 + df)) + 1
  const total = movies.length;
  return docs.map((doc) => {
    const counts = new Map();
    for (const word of doc) counts.set(word, (counts.get(word) || 0) + 1);

    const vector = new Map();
    let lengthSquared = 0;
    for (const [word, count] of counts) {
      const idf = Math.log((1 + total) / (1 + docFreq.get(word))) + 1;
      const weight = count * idf;
      vector.set(word, weight);
      lengthSquared += weight * weight;
    }
    // Normalise to length 1, so cosine similarity is just a dot product.
    const length = Math.sqrt(lengthSquared) || 1;
    for (const [word, weight] of vector) vector.set(word, weight / length);
    return vector;
  });
}

// Cosine similarity between two normalised vectors = their dot product.
function similarity(vectorA, vectorB) {
  let sum = 0;
  for (const [word, weight] of vectorA) {
    if (vectorB.has(word)) sum += weight * vectorB.get(word);
  }
  return sum;
}

// Return the top N most similar movies to the named one.
function recommend(title, movies, vectors, topN = 5) {
  const index = movies.findIndex(
    (movie) => movie.title.toLowerCase() === title.toLowerCase()
  );
  if (index === -1) return [];

  const scored = movies
    .map((movie, i) => ({ movie, score: similarity(vectors[index], vectors[i]) }))
    .filter((entry) => entry.movie.title !== movies[index].title)
    .sort((a, b) => b.score - a.score);
  return scored.slice(0, topN);
}

// ---- Page wiring (browser only) ----
if (typeof document !== "undefined") {
  const vectors = buildVectors(MOVIES);
  const select = document.getElementById("movie-select");
  const list = document.getElementById("results");

  // Fill the dropdown with all 60 titles, sorted A-Z.
  const sorted = [...MOVIES].sort((a, b) => a.title.localeCompare(b.title));
  for (const movie of sorted) {
    const option = document.createElement("option");
    option.value = movie.title;
    option.textContent = `${movie.title} (${movie.year})`;
    select.appendChild(option);
  }

  function showRecommendations() {
    const picks = recommend(select.value, MOVIES, vectors, 5);
    list.innerHTML = "";
    for (const pick of picks) {
      const item = document.createElement("li");
      const percent = Math.round(pick.score * 1000) / 10;
      item.innerHTML =
        `<span class="title"></span> <span class="meta"></span>` +
        `<span class="bar"><span style="width:${percent}%"></span></span>` +
        `<span class="score">${percent}% similar</span>`;
      item.querySelector(".title").textContent = pick.movie.title;
      item.querySelector(".meta").textContent =
        `${pick.movie.year} · ${pick.movie.genres}`;
      list.appendChild(item);
    }
  }

  select.value = "3 Idiots";
  select.addEventListener("change", showRecommendations);
  showRecommendations();
}

// Allow the Node.js verification script to use the same functions.
if (typeof module !== "undefined") {
  module.exports = { tokenize, buildVectors, similarity, recommend };
}
