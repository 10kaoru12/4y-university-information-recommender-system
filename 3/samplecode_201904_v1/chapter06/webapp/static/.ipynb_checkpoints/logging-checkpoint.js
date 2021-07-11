
const logSendHandler = function(event) {
    const elm = event.currentTarget || event.target;
    // DOMにdata-contextがある場合、それらの情報を埋め込む
    const context = elm.dataset && elm.dataset.context && JSON.parse(elm.dataset.context) || {}
    const payload = {
       "event": event.type,            
       "context": context,
       "timestamp": (new Date().getTime()),
       "referrer": document.referrer,
       "target": event.target.nodeName,
    }  
    data = JSON.stringify(payload);
    
    // debug用
    console.log(data);
    
    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/log', true);
    xhr.setRequestHeader("Content-Type", "application/json");        
    xhr.send(data); 
};

document.addEventListener("DOMContentLoaded", logSendHandler);        

// DOMの読み込み後に画像にイベントハンドラを仕込む
document.addEventListener("DOMContentLoaded",
  () => {      
    document.querySelectorAll(".book-item")
      .forEach((elm) => {
          logSendHandler({type: "load", target: elm})
          elm.addEventListener("click", logSendHandler);
      });      
  }
);