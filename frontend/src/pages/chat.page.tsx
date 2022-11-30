import { Component, createSignal, For, onMount, Show } from "solid-js";

import { AiTwotoneSetting } from "../components/icons/AiTwotoneSetting";
import { addEmojisToString } from "../lib/emojiMap";
import { Message, OnInput, OnKeyPress, Ref } from "../types";
import { getGlobalUser, setGlobalUser } from "../services/auth.service";

const users = [
  { id: 1, name: "user1" },
  { id: 2, name: "user2" },
  { id: 3, name: "user3" },
  { id: 4, name: "user4" },
];

export const ChatPage: Component = () => {
  const [messages, setMessages] = createSignal<Message[]>([], {
    name: "messages",
  });
  const [message, setMessage] = createSignal("", { name: "message" });
  const [isModalOpen, setIsModalOpen] = createSignal(false, {
    name: "isModalOpen",
  });

  // eslint-disable-next-line prefer-const
  let ref: Ref<HTMLDivElement> = null;

  onMount(() => {
    const auth = {
      id: 12,
      name: "Gabryjiel",
    };

    setGlobalUser(auth);
  });

  const handleOnKeyPress: OnKeyPress = (event) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();

      const newMessage: Message = {
        id: 1,
        user: getGlobalUser(),
        content: message(),
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, newMessage]);
      setMessage("");
      ref.scroll({ top: ref.scrollHeight });
    }
  };

  const handleOnInput: OnInput = (event) => {
    if (event.inputType === "insertText") {
      setMessage(addEmojisToString(event.currentTarget.value));
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
          class="flex h-11/12 w-full flex-col gap-2 overflow-y-auto overflow-x-hidden border-b-2 border-stone-700"
        >
          <For each={messages()} fallback={<div>No messages yet</div>}>
            {(item, index) => (
              <div id={`message-${index()}`} class="flex w-full flex-col px-2">
                <div class="flex items-center gap-2">
                  <span class="font-bold">{item.user.name}</span>
                  <span class="flex-1 break-all">{item.content}</span>
                </div>
                <span class="w-full text-right italic">
                  {item.timestamp.toLocaleString()}
                </span>
              </div>
            )}
          </For>
        </div>
        <div class="h-1/12 w-full p-2">
          <textarea
            class="h-full w-full resize-none bg-stone-200"
            value={message()}
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
        <div
          onClick={handleEventToggle}
          class="absolute flex h-screen w-screen items-center justify-center"
          style={{ "background-color": "rgba(0,0,0,0.67)" }}
        >
          <div
            class="h-2/3 w-2/3 rounded-lg border-4 border-stone-800 bg-stone-500 opacity-100"
            onClick={(event) => {
              event.preventDefault();
              event.stopPropagation();
            }}
          />
        </div>
      </Show>
    </div>
  );
};
