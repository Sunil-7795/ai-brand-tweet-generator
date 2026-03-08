let generatedTweets=[]

async function generateTweets(){

document.getElementById("loading").style.display="block"

let brand=document.getElementById("brand").value
let industry=document.getElementById("industry").value
let objective=document.getElementById("objective").value
let product=document.getElementById("product").value

let response=await fetch("/generate",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
brand:brand,
industry:industry,
objective:objective,
product:product
})

})

let data=await response.json()

document.getElementById("loading").style.display="none"

let voiceText = data.voice.split("\n")

let voiceHTML=""

voiceText.forEach(line=>{

if(line.trim()!=""){

voiceHTML+=`
<div class="voice-item">
<div class="voice-title">Brand Insight</div>
${line}
</div>
`

}

})

document.getElementById("voice").innerHTML=voiceHTML

let tweets=data.tweets.split("\n")

generatedTweets=tweets

let html=""

tweets.forEach(tweet=>{

if(tweet.trim()!=""){

html+=`
<div class="tweet-card">

<b>${brand} ✔</b>

<p>${tweet}</p>

<button class="copy-btn" onclick="copyTweet('${tweet}')">Copy</button>

</div>
`

}

})

document.getElementById("tweets").innerHTML=html

}

function copyTweet(tweet){

navigator.clipboard.writeText(tweet)

alert("Tweet copied!")

}

function downloadTweets(){

let text=generatedTweets.join("\n")

let blob=new Blob([text],{type:"text/plain"})

let link=document.createElement("a")

link.href=URL.createObjectURL(blob)

link.download="generated_tweets.txt"

link.click()

}

function toggleTheme(){

document.body.classList.toggle("dark")

}