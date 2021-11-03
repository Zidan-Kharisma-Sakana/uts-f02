function createChatBlock(obj, teman) {
  let outerBlok = document.createElement('div')
  outerBlok.classList.add("chat-outer")
  let name = document.createElement("h5")
  let content = document.createElement("div")
  outerBlok.appendChild(name)
  outerBlok.appendChild(content)
  if (obj["penerima"] === teman) {
    // kita yang kirim
    outerBlok.classList.add("end")
    name.classList.add("your-title")
    name.innerText = "You"
    content.classList.add("your-message")
    content.innerText = obj["isi"]
    content.classList.add("isi")
    content.classList.add("end")
    return outerBlok
  }
  name.classList.add("their-title")
  name.innerText = obj['pengirim']
  content.classList.add("their-message")
  content.innerText = obj["isi"]
  return outerBlok
  // teman yang kirim
}

function main() {
  const messages_container = document.getElementById("chat_box");
  let dm_id = document.getElementById("dm_id").value;
  console.log(dm_id);
  let nama_teman = document.getElementById("nama_teman").value;
  let nama_saya = document.getElementById("nama_saya").value;

  let chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/realchat/" + dm_id + "/"
  );

  chatSocket.onopen = function (e) {
    console.log("WebSocket Opened");
    chatSocket.send(
      JSON.stringify({
        isi: "get-history",
        content_lain: "content lain",
      })
    );
  };

  chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log(e);
    let message = data["message"];
    console.log(message["type"]);
    if (message["type"] === "get-history") {
      let history = message["history"]
      if(!!history){
        console.log(history)
        history.forEach(element => {
          messages_container.appendChild(createChatBlock(element, nama_teman, false))
        });
      
      }
      
    } else{
      console.log(message)
      
      messages_container.appendChild(createChatBlock(message['isi'], nama_teman, true))
    }
    messages_container.scrollTop = messages_container.scrollHeight
  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  sendButton = document.getElementById("sendButton");
  sendButton.addEventListener("click", (e) => {
    messageContent = document.getElementById("messageContent");
    let msg = messageContent.value;
    console.log(msg);
    chatSocket.send(
      JSON.stringify({
        isi: msg,
        pengirim: nama_saya,
        penerima: nama_teman
      })
    );
    messageContent.value = "";
  });
}
document.addEventListener("DOMContentLoaded", function (event) {
  main();
});
