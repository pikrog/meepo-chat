import { A, useNavigate } from "@solidjs/router";
import { Component, createSignal, For, Match, onMount, Switch } from "solid-js";

import { AiFillEye } from "../components/icons/AiFillEye";
import { AiFillEyeInvisible } from "../components/icons/AiFillEyeInvisible";
import { setServerAddress } from "../services/chat.service";
import { type GetServer, getServers } from "../services/ky.service";

export type OnSubmitEvent = Event & {
  submitter: HTMLElement;
} & {
  currentTarget: HTMLFormElement;
  target: Element;
};

export const SelectPage: Component = () => {
  const navigate = useNavigate();

  const [servers, setServers] = createSignal<GetServer[]>([
    { serverId: 1, address: 'localhost:8000', name: 'Ohio' },
    { serverId: 2, address: 'localhost:8001', name: 'Frankfurt' },
    { serverId: 3, address: 'localhost:8002', name: 'Wellington' }
  ], { name: "servers" });

  const handleServerChoice = async (serverAddress: string) => {
    setServerAddress(serverAddress);
    navigate('/chat');
  };

  onMount(async () => {
    // const response = await getServers()
    // setServers(response);
  });

  return (
    <div class="grid h-screen w-screen place-items-center">
      <div
        class="flex h-3/5 w-1/2 flex-col items-center justify-evenly gap-2 rounded-lg border-4 border-stone-600 bg-stone-200 p-8"
      >
        <div>Logo</div>
        <div class="flex w-full flex-col gap-2 overflow-hidden">
          <div class="w-full text-center">
            <span class="font-bold text-xl">Wybierz serwer</span>
          </div>
          <div class="flex flex-col gap-2 overflow-y-auto h-80 items-center justify-center">
            <For each={servers()}>
              {(item) => (
                <div onClick={() => handleServerChoice(item.address)} class="flex w-full justify-between border-4 border-stone-700 p-2 rounded-lg bg-stone-300 hover:brightness-105 cursor-pointer">
                  <div class="font-bold">{item.name}</div>
                  <div class="italic">{item.address}</div>
                </div>
              )}
            </For>
          </div>
        </div>
      </div>
    </div>
  );
};
