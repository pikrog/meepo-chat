import { Component, createSignal, For, Match, Switch } from "solid-js";

export const SettingsModal: Component<{
  closeModal: (event: MouseEvent) => void;
}> = (props) => {
  const tabs = [
    { id: "server", label: "Serwer" },
    { id: "account", label: "Konto" },
  ] as const;

  const servers = ["Ohio", "Frankfurt", "Sydney"] as const;

  type Tabs = typeof tabs[number]["id"];

  const [tab, setTab] = createSignal<Tabs>("server", { name: "tab" });
  const [selectedServer, setSelectedServer] = createSignal<string | null>(
    null,
    {
      name: "selectedServer",
    }
  );

  return (
    <div
      onClick={(event) => props.closeModal(event)}
      class="absolute flex h-screen w-screen items-center justify-center"
      style={{ "background-color": "rgba(0,0,0,0.67)" }}
    >
      <div
        class="flex h-2/3 w-2/3 flex-col rounded-lg border-4 border-stone-800 bg-stone-300 p-2 opacity-100"
        onClick={(event) => {
          event.preventDefault();
          event.stopPropagation();
        }}
      >
        <div class="flex justify-between border-b-2 border-stone-700">
          <For each={tabs}>
            {(item) => (
              <button
                onClick={() => setTab(item.id)}
                class={`flex-1 border-r-2 border-stone-700 p-2 text-center text-xl font-bold last:border-0 ${
                  tab() === item.id ? "text-lime-600" : ""
                }`}
              >
                {item.label}
              </button>
            )}
          </For>
        </div>

        <div class="h-full w-full p-4">
          <Switch>
            <Match when={tab() === "server"}>
              <div class="flex h-10/12 w-full flex-col border-2 border-stone-700">
                <For each={servers}>
                  {(item) => (
                    <div
                      class={`w-full cursor-pointer p-2 text-center text-xl font-semibold ${
                        selectedServer() === item ? "bg-stone-400" : ""
                      }`}
                      onClick={() =>
                        setSelectedServer((prev) =>
                          item === prev ? null : item
                        )
                      }
                    >
                      {item}
                    </div>
                  )}
                </For>
              </div>
              <div class="h-2/12 pt-2">
                <div class="flex h-full w-full items-center justify-around">
                  <button class="h-16 w-32 rounded-lg border-4 border-stone-900 bg-lime-700 text-xl font-bold text-stone-200 hover:brightness-105">
                    Rozłącz
                  </button>
                  <button
                    class={`h-16 w-32 rounded-lg border-4 border-stone-900 text-xl font-bold text-stone-200 ${
                      selectedServer() === null
                        ? "border-stone-400 bg-stone-300 text-stone-400"
                        : "bg-lime-700 hover:brightness-105"
                    }`}
                    disabled={selectedServer() === null}
                  >
                    Połącz
                  </button>
                </div>
              </div>
            </Match>
            <Match when={tab() === "account"}>
              <div />
            </Match>
          </Switch>
        </div>
      </div>
    </div>
  );
};
