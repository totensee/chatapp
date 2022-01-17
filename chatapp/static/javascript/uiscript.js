const innerWrapper = document.getElementById("inner-wrapper");
innerWrapper.scrollTop = innerWrapper.scrollHeight - innerWrapper.clientHeight;

(async () => {
    const rawResponse = await fetch('http://127.0.0.1:5000/api/send/channel', {
      method: 'POST',
      body: JSON.stringify({a: 1, b: 'Textual content'})
    });
    const content = await rawResponse.json();
  
    console.log(content);
})();