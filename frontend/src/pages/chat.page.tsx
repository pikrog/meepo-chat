import { Component, createSignal, For, onMount, Show, onCleanup } from "solid-js";

import { AiTwotoneSetting } from "../components/icons/AiTwotoneSetting";
import { addEmojisToString } from "../lib/emojiMap";
import { Message, OnInput, OnKeyPress, Ref, TextChatMessage, WSMessage } from "../types";
import { getAccessToken, setAccessToken } from "../services/auth.service";
import { SettingsModal } from "../components/SettingsModal";
import { disconnectFromWebSocket, getUserList, getWebSocket, sendChatMessage, setNewWebSocket } from "../services/websocket.service";
import { getServerMessage } from "../services/ky.service";
import { getServerAddress } from "../services/chat.service";
import { getFromLocalStorage } from "../services/local-storage.service";

const users = [
  { id: 1, name: "user1" },
  { id: 2, name: "user2" },
  { id: 3, name: "user3" },
  { id: 4, name: "user4" },
];

export const ChatPage: Component = () => {
  const [messages, setMessages] = createSignal<WSMessage[]>([], {
    name: "messages",
  });
  const [text, setText] = createSignal("", { name: "text" });
  const [isModalOpen, setIsModalOpen] = createSignal(false, {
    name: "isModalOpen",
  });
  const [userList, setUserList] = createSignal<string[]>([], { name: "userList" })

  let websocket = getWebSocket();

  const handleWebSocketMessage = (message: MessageEvent<string>) => {
    const data = JSON.parse(message.data) as WSMessage;
    
    if (data.opcode === 'chat') {
      if (data.data.type === 'leave') {
        setUserList((prev) => prev.filter((name) => name !== data.data.sender));
      } else if (data.data.type === 'join') {
        setUserList((prev) => prev.concat([data.data.sender]));
      }
    }

    if (data.opcode === 'user_list') {
      setUserList(data.data.map((item) => item.name));
    } else {
      setMessages((prev) => prev.concat([data]));
      ref.scroll({ top: ref.scrollHeight });
    }
  }

  if (websocket) {
    websocket.onmessage = handleWebSocketMessage;
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

  const handleEventToggle = (event: MouseEvent) => {
    event.preventDefault();
    setIsModalOpen((prev) => !prev);
  };

  onMount(async () => {
    if (!websocket) {
      websocket = await setNewWebSocket(getServerAddress());
      websocket.onmessage = handleWebSocketMessage;
    }
    getUserList(websocket);

    const response = await getServerMessage(getServerAddress());
    const worthyMessages: WSMessage[] = response
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
    console.log("END M<E")
    disconnectFromWebSocket();
  })

  return (
    <div class="flex h-screen w-screen">
      <main class="h-screen flex-1">
        <div
          ref={ref}
          class="flex h-11/12 w-full flex-col gap-1 overflow-y-auto overflow-x-hidden border-b-2 border-stone-700"
        >
          <For each={messages()} fallback={<div>No messages yet</div>}>
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
          <button onClick={handleEventToggle}>
            <AiTwotoneSetting width="4em" height="4em" />
          </button>
        </div>
      </aside>

      <Show when={isModalOpen() === true}>
        <SettingsModal closeModal={handleEventToggle} />
      </Show>
    </div>
  );
};
