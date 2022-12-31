import { Component, createSignal, For, onMount, Show } from "solid-js";

import { AiTwotoneSetting } from "../components/icons/AiTwotoneSetting";
import { addEmojisToString } from "../lib/emojiMap";
import { Message, OnInput, OnKeyPress, Ref, WSMessage } from "../types";
import { getAccessToken, setAccessToken } from "../services/auth.service";
import { SettingsModal } from "../components/SettingsModal";
import { getWebSocket, sendChatMessage } from "../services/websocket.service";

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

  const websocket = getWebSocket();

  websocket.onmessage = (message: MessageEvent<string>) => {
    const data = JSON.parse(message.data) as WSMessage;
    setMessages((prev) => prev.concat([data]));
  };

  // eslint-disable-next-line prefer-const
  let ref: Ref<HTMLDivElement> = null;

  const handleOnKeyPress: OnKeyPress = (event) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();

      const newMessage: Message = {
        id: 1,
        user: {id: 1, name: 'me'},
        content: text(),
        timestamp: new Date(),
      };

      sendChatMessage(text());
      setText("");
      ref.scroll({ top: ref.scrollHeight });
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
          <For each={users} fallback={<div>No other users</div>}>
            {(item) => <div id={`aside-user-${item.id}`}>{item.name}</div>}
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
