// ---- Supported languages (code : label) ----
const LANGUAGES = {
  en: "English", es: "Spanish", fr: "French", de: "German", it: "Italian",
  pt: "Portuguese", hi: "Hindi", mr: "Marathi", bn: "Bengali", ta: "Tamil",
  te: "Telugu", gu: "Gujarati", zh: "Chinese", ja: "Japanese", ko: "Korean",
  ar: "Arabic", ru: "Russian", nl: "Dutch", tr: "Turkish", vi: "Vietnamese"
};

const sourceSel = document.getElementById("sourceLang");
const targetSel = document.getElementById("targetLang");
const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");
const charCount = document.getElementById("charCount");
const translateBtn = document.getElementById("translateBtn");
const statusMsg = document.getElementById("statusMsg");
const copyBtn = document.getElementById("copyBtn");
const listenInputBtn = document.getElementById("listenInputBtn");
const listenOutputBtn = document.getElementById("listenOutputBtn");
const swapBtn = document.getElementById("swapBtn");

function populateSelects(){
  Object.entries(LANGUAGES).forEach(([code, label]) => {
    const opt1 = document.createElement("option");
    opt1.value = code; opt1.textContent = label;
    sourceSel.appendChild(opt1);

    const opt2 = document.createElement("option");
    opt2.value = code; opt2.textContent = label;
    targetSel.appendChild(opt2);
  });
  sourceSel.value = "en";
  targetSel.value = "hi";
}
populateSelects();

inputText.addEventListener("input", () => {
  charCount.textContent = `${inputText.value.length} / 1000`;
});

swapBtn.addEventListener("click", () => {
  swapBtn.classList.add("spin");
  setTimeout(() => swapBtn.classList.remove("spin"), 150);
  const s = sourceSel.value;
  sourceSel.value = targetSel.value;
  targetSel.value = s;
});

// ---- Translation call ----
// Using MyMemory Translation API: free, no API key required, CORS-enabled,
// and works fine from a plain local page (e.g. VS Code's "Live Server").
// This is the client-side option. If your project specifically requires
// Google Translate API or Microsoft Translator (both need a paid/free-tier
// API key), use the small Node backend included in /backend-optional
// instead — see its README for setup, then swap the fetch below for a call
// to your own backend endpoint (e.g. http://localhost:3000/translate).
async function translateText(text, sourceLang, targetLang){
  const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${sourceLang}|${targetLang}`;
  const res = await fetch(url);
  if(!res.ok) throw new Error("Network error while contacting the translation service.");
  const data = await res.json();
  if(!data || !data.responseData || typeof data.responseData.translatedText !== "string"){
    throw new Error("Unexpected response from the translation service.");
  }
  return data.responseData.translatedText;
}

async function handleTranslate(){
  const text = inputText.value.trim();
  if(!text){
    statusMsg.textContent = "Type something to translate.";
    statusMsg.classList.remove("error");
    return;
  }
  const sourceLang = sourceSel.value;
  const targetLang = targetSel.value;

  translateBtn.disabled = true;
  statusMsg.textContent = "Translating...";
  statusMsg.classList.remove("error");
  outputText.classList.add("placeholder");
  outputText.textContent = "Translating...";

  try{
    const translated = await translateText(text, sourceLang, targetLang);
    outputText.textContent = translated;
    outputText.classList.remove("placeholder");
    copyBtn.disabled = false;
    listenOutputBtn.disabled = false;
    statusMsg.textContent = "";
  }catch(err){
    outputText.textContent = "Your translation will appear here.";
    outputText.classList.add("placeholder");
    copyBtn.disabled = true;
    listenOutputBtn.disabled = true;
    statusMsg.textContent = err.message || "Something went wrong. Try again.";
    statusMsg.classList.add("error");
  }finally{
    translateBtn.disabled = false;
  }
}
translateBtn.addEventListener("click", handleTranslate);

// ---- Copy button ----
copyBtn.addEventListener("click", async () => {
  try{
    await navigator.clipboard.writeText(outputText.textContent);
    const original = copyBtn.textContent;
    copyBtn.textContent = "✓ Copied";
    setTimeout(() => { copyBtn.textContent = original; }, 1500);
  }catch(err){
    statusMsg.textContent = "Couldn't copy — select and copy manually.";
    statusMsg.classList.add("error");
  }
});

// ---- Text-to-speech ----
function speak(text, langCode){
  if(!("speechSynthesis" in window)){
    statusMsg.textContent = "Text-to-speech isn't supported in this browser.";
    statusMsg.classList.add("error");
    return;
  }
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = langCode;
  window.speechSynthesis.speak(utter);
}
listenInputBtn.addEventListener("click", () => {
  if(inputText.value.trim()) speak(inputText.value, sourceSel.value);
});
listenOutputBtn.addEventListener("click", () => {
  if(outputText.textContent) speak(outputText.textContent, targetSel.value);
});
