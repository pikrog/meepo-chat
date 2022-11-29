import { Component, createSignal, For } from 'solid-js';

type OnKeyPressEvent = KeyboardEvent & {
  currentTarget: HTMLTextAreaElement;
  target: Element;
};

export const App: Component = () => {
  const [messages, setMessages] = createSignal<string[]>([], {name: 'messages'})
  const [message, setMessage] = createSignal('', {name: 'message'});

  const handleKeyPress = (event: OnKeyPressEvent) => {
    const { value }  =  event.currentTarget;

    if (event.key !== 'Enter') {
      return setMessage(value)
    }

    event.preventDefault()

    setMessages((prev) => [...prev, value])
    setMessage("")
  }

  return (
    <div class="h-screen w-screen bg-slate-500 flex">
      <main class="h-screen flex-1">
        <div class="flex h-128 flex-col w-full">
          <For each={messages()} fallback={<div>No messages yet</div>}>
            {(item, index) => <div id={`message-${index()}`}>{item}</div>}
          </For>
        </div>
        <textarea
          class='resize-none' 
          value={message()} 
          onKeyPress={handleKeyPress}
        />
      </main>
      <nav class="h-screen w-24 border-l-2 border-slate-200">
        <div>a</div>
        <div>b</div>
      </nav>
    </div>
  );
};
