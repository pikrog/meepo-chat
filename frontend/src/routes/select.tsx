import { createSignal, For, onCleanup, onMount, Show } from "solid-js";
import { Button } from "../components/Button";

import { redirectToLoginIfNotLoggedIn, setAccessToken } from "../services/auth.service";
import { setServerAddress } from "../services/chat.service";
import { FullServerInfo, getServerInfo, getServers, ServerInfo } from "../services/fetch.service";

import MeepoChatLogo from '../../public/meepo-chat-logo.png';
import { setInLocalStorage } from "../services/local-storage.service";
import { useNavigate } from "solid-start";
import { getWSError, setWSError } from "../services/websocket.service";
import { filterOutEmpty } from "../lib/util";

export type OnSubmitEvent = Event & {
  submitter: HTMLElement;
} & {
  currentTarget: HTMLFormElement;
  target: Element;
};

export default function SelectPage() {
  const navigate = useNavigate();

  const [servers, setServers] = createSignal<FullServerInfo[]>([], { name: "servers" });

  const handleServerChoice = async (serverAddress: string) => {
    try {
      setServerAddress(serverAddress);
      setInLocalStorage('server_address', serverAddress);
      navigate('/chat');
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = () => {
    setAccessToken('');
    setInLocalStorage('access_token', '');
    navigate('/login');
  };

  const fetchServers = async () => {
    if (typeof window !== 'undefined') {
      const response = await getServers()
      const servers = await Promise.all(
        response.map(async (server, idx) => {
          try {
            const serverInfo = await getServerInfo(server.address)

            return {
              ...serverInfo,
              ...response[idx]
            }
          } catch (error) {
            return null;
          }
        })
      );

      const filteredServers = servers.filter(filterOutEmpty);
      
      setServers(filteredServers);
    }
  };

  let interval: NodeJS.Timer | undefined = undefined;


  onMount(() => {
    redirectToLoginIfNotLoggedIn(navigate);
    fetchServers();
    interval = setInterval(() => {
      fetchServers();
    }, 5000);
  });

  onCleanup(() => {
    setWSError('');
    clearInterval(interval);
  });

  return (
    <div class="grid h-screen w-screen place-items-center">
      <div
        class="flex h-4/5 w-1/2 flex-col items-center justify-evenly gap-2 rounded-lg border-4 border-stone-600 bg-stone-200 p-8"
      >
        <img src={MeepoChatLogo} alt="Meepo Chat Logo" />
        <div class="flex w-full flex-col gap-2 overflow-hidden">
          <div class="w-full text-center">
            <span class="font-bold text-xl">Wybierz serwer</span>
          </div>
          <div class="flex flex-col gap-2 overflow-y-auto h-80 items-center justify-center">
            <For each={servers()}>
              {(item) => (
                <div onClick={() => handleServerChoice(item.address)} class="flex w-full justify-between border-4 border-stone-700 p-2 rounded-lg bg-stone-300 hover:brightness-105 cursor-pointer">
                  <div class="flex gap-1">
                    <span class="font-bold">{item.server_name}</span>
                    <span>{`(${item.num_clients} / ${item.max_clients})`}</span>
                  </div>
                  <div class="italic">{item.address}</div>
                </div>
              )}
            </For>
          </div>
          <div class="w-full flex justify-center">
            <Button onClick={handleLogout} text="Wyloguj się" />
          </div>
          <Show when={getWSError().length > 0}>
            <div class="w-full flex justify-center">
              <span class="text-red-500 text-xl">{getWSError()}</span>
            </div>
          </Show>
        </div>
      </div>
    </div>
  );
};
