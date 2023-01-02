import { Component, createSignal, For, onMount, Show, onCleanup } from "solid-js";

import { addEmojisToString } from "../lib/emojiMap";
import { ChatMessage, OnInput, OnKeyPress, Ref, WSMessage } from "../types";
import { disconnectFromWebSocket, getUserList, getWebSocket, sendChatMessage, setNewWebSocket } from "../services/websocket.service";
import { getServerMessage } from "../services/fetch.service";
import { getServerAddress } from "../services/chat.service";
import { useNavigate } from "@solidjs/router";
import { setSelectPageError } from "./select.page";

export const ChatPage: Component = () => {
  const [messages, setMessages] = createSignal<ChatMessage[]>([], {
    name: "messages",
  });
  const [text, setText] = createSignal("", { name: "text" });
  const [userList, setUserList] = createSignal<string[]>([], { name: "userList" })

  const navigate = useNavigate();
  
  const handleWebSocketMessage = (message: MessageEvent<string>) => {
    const data = JSON.parse(message.data) as WSMessage;
    console.log(data);
    if (data.opcode === 'chat') {
      if (data.data.type === 'leave') {
        setUserList((prev) => prev.filter((name) => name !== data.data.sender));
      } else if (data.data.type === 'join') {
        setUserList((prev) => prev.concat([data.data.sender]));
      }

      setMessages((prev) => prev.concat([data]));
      ref.scroll({ top: ref.scrollHeight });
    } else if (data.opcode === 'user_list') {
      setUserList(data.data.map((item) => item.name));
    } else if (data.opcode === 'error') {
      setSelectPageError(data.data);
    }
  }
  
  let websocket = getWebSocket();

  if (websocket) {
    websocket.onmessage = handleWebSocketMessage;
    websocket.onclose = (event) => {
      console.dir(event);
      navigate('/select');
    }
  }

  // eslint-disable-next-line prefer-const
  let ref: Ref<HTMLDivElement> = null;

  const handleOnKeyPress: OnKeyPress = (event) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();

      sendChatMessage(text());
      setText("");
    }
  };

  const handleOnInput: OnInput = (event) => {
    if (event.inputType === "insertText") {
      setText(addEmojisToString(event.currentTarget.value));
    }
  };

  onMount(async () => {
    if (!websocket) {
      websocket = await setNewWebSocket(getServerAddress());
      websocket.onmessage = handleWebSocketMessage;
    }
    getUserList(websocket);

    const response = await getServerMessage(getServerAddress());
    const worthyMessages: ChatMessage[] = response
      .filter((message) => message.type === 'chat' && message.text !== null)
      .map((message) => ({
        opcode: 'chat',
        data: {
          type: 'chat',
          sender: message.sender,
          text: message.text,
          timestamp: message.timestamp
        },
      }));
    worthyMessages.reverse();
    setMessages((prev) => worthyMessages.concat(prev));
    ref.scroll({ top: ref.scrollHeight });
  });

  onCleanup(() => {
    disconnectFromWebSocket();
  })

  return (
    <div class="flex h-screen w-screen">
      <main class="h-screen flex-1">
        <div
          ref={ref}
          class="flex h-11/12 w-full flex-col gap-1 overflow-y-auto overflow-x-hidden border-b-2 border-stone-700"
        >
          <For each={messages()} fallback={<div>Brak wiadomości</div>}>
            {(item, index) => {
              const timestamp = new Date(item.data.timestamp).toLocaleString();

              if (item.data.type === 'chat') {
                return (
                  <div id={`message-${index()}`} class="flex w-full px-2">
                    <div class="flex flex-1 items-center gap-2">
                      <span class="font-bold">{item.data.sender}</span>
                      <span class="flex-1 break-all">{addEmojisToString(item.data.text)}</span>
                    </div>
                    <div class="w-36">
                      <span class="w-full text-right italic">
                        {timestamp}
                      </span>
                    </div>
                  </div>
                );
              } else if (item.data.type === 'join') {
                return (
                  <div id={`message-${index()}`} class="flex w-full px-2">
                    <div class="flex flex-1 items-center gap-2">
                      <span class="italic">{`${item.data.sender} dołączył do serwera`}</span>
                    </div>
                    <div class="w-36">
                      <span class="w-full text-right italic">
                        {timestamp}
                      </span>
                    </div>
                  </div>
                );
              } else if (item.data.type === 'leave') {
                return (
                  <div id={`message-${index()}`} class="flex w-full px-2">
                    <div class="flex flex-1 items-center gap-2">
                      <span class="italic">{`${item.data.sender} opuścił serwer`}</span>
                    </div>
                    <div class="w-36">
                      <span class="w-full text-right italic">
                        {timestamp}
                      </span>
                    </div>
                  </div>
                );
              } else {
                return <hr />;
              }
            }}
          </For>
        </div>
        <div class="h-1/12 w-full p-2">
          <textarea
            class="h-full w-full resize-none bg-stone-200"
            value={text()}
            onInput={handleOnInput}
            onKeyPress={handleOnKeyPress}
          />
        </div>
      </main>
      <aside class="flex h-full w-48 flex-col border-l-2 border-stone-700 indent-2">
        <div class="h-11/12">
          <div class="font-bold">Lista użytkowników</div>
          <For each={userList()} fallback={<div>Brak użytkowników</div>}>
            {(item) => <div id={`aside-user-${item}`}>{item}</div>}
          </For>
        </div>
        <div class="flex h-1/12 items-center justify-center">
          <button
            class="border-4 w-32 p-2 border-lime-900 bg-lime-500 hover:brightness-105 rounded-lg"
            onClick={() => navigate('/select')}
          >
            Rozłącz
          </button>
        </div>
      </aside>
    </div>
  );
};
