import { createSignal, For, onMount, onCleanup, Show } from "solid-js";

import { addEmojisToString } from "../lib/emojiMap";
import { OnInput, OnKeyPress, Ref } from "../types";
import { ChatServerWebSocket, getMessages, getUserList, getWSError, setShouldReconnect, setWSError, shouldReconnect } from "../services/websocket.service";
import { getFromLocalStorage } from "../services/local-storage.service";
import { useNavigate } from "solid-start";
import { redirectToLoginIfNotLoggedIn } from "../services/auth.service";
import { Spinner } from "../components/Spinner";

export default function ChatPage() {
  const navigate = useNavigate();
  const [text, setText] = createSignal("", { name: "text" });
  const [isClosed, setIsClosed] = createSignal(false, { name: "isClosed" });
  let reconnetCount = 0;
  // eslint-disable-next-line prefer-const
  let ref: Ref<HTMLDivElement> | undefined = undefined;

  let chatServer: ChatServerWebSocket | undefined;

  const handleOnKeyPress: OnKeyPress = (event) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();

      chatServer?.postChatMessage(text());
      setText("");
    }
  };

  const handleOnInput: OnInput = (event) => {
    if (event.inputType === "insertText") {
      setText(addEmojisToString(event.currentTarget.value));
    } else if (event.inputType === "insertFromPaste") {
      setText((prev) => prev + event.data);
    }
  };

  const handleLeave = () => {
    setShouldReconnect(false);
    setWSError('');
    navigate('/select');
  };

  onMount(async () => {
    reconnetCount = 0;
    redirectToLoginIfNotLoggedIn(navigate);

    chatServer = new ChatServerWebSocket(getFromLocalStorage('server_address') ?? '', {
      onChatMessage: () => {
        ref?.scrollTo({ top: ref.scrollHeight });
      },
      onOpen: () => {
        setIsClosed(false);
        chatServer?.fetchUserList();
        chatServer?.fetchMessages();
      },
      onMessages: () => {
        ref?.scrollTo({ top: ref.scrollHeight });
      },
      onClose: () => {
        setIsClosed(true);

        if (shouldReconnect() && reconnetCount < 10) {
          chatServer?.reconnect();
          reconnetCount++;
        } else {
          navigate('/select');
        }
       }
    });

  });

  onCleanup(() => {
    chatServer?.closeWebSocket();
    chatServer?.cleanUserList();
    chatServer?.cleanMessages();
  })

  return (
    <div class="flex h-screen w-screen relative">
      <Show when={isClosed()}>
        <div class="absolute z-10 w-full h-full grid place-items-center" style={{ "background-color": 'rgba(0, 0, 0, 0.5)'}}>
          <div class="bg-stone-200 p-8 rounded-xl flex items-center justify-center flex-col gap-2">
            <div class="flex">
              <span class="text-red-500 text-2xl font-bold">Nie mo??na po????czy?? si?? z serwerem</span>
              <Spinner />
            </div>
            <button
              class="border-4 w-32 p-2 border-lime-900 bg-lime-500 hover:brightness-105 rounded-lg"
              onClick={handleLeave}
            >
              Roz????cz
            </button> 
          </div>
        </div>
      </Show>
      <main class="h-screen flex-1">
        <div
          ref={ref}
          class="flex h-11/12 w-full flex-col gap-1 overflow-y-auto overflow-x-hidden border-b-2 border-stone-700"
        >
          <For each={getMessages()} fallback={<div>Brak wiadomo??ci</div>}>
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
                      <span class="italic">{`${item.data.sender} do????czy?? do serwera`}</span>
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
                      <span class="italic">{`${item.data.sender} opu??ci?? serwer`}</span>
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
          <div class="font-bold">Lista u??ytkownik??w</div>
          <For each={getUserList()} fallback={<div>Brak u??ytkownik??w</div>}>
            {(item) => <div id={`aside-user-${item}`}>{item}</div>}
          </For>
        </div>
        <div class="flex h-1/12 items-center justify-center">
          <button
            class="border-4 w-32 p-2 border-lime-900 bg-lime-500 hover:brightness-105 rounded-lg"
            onClick={handleLeave}
          >
            Roz????cz
          </button>
        </div>
      </aside>
    </div>
  );
};
