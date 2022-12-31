import { createSignal } from "solid-js";
import { getAccessToken } from "./auth.service";

export const [getWebSocket, setWebSocket] = createSignal<null | WebSocket>(null, {
  name: "websocket",
});

export function setNewWebSocket(serverAddress: string): Promise<WebSocket> {
  return new Promise((resolve, reject) => {
    const ws = setWebSocket(new WebSocket(`ws://${serverAddress}/ws?access_token=${getAccessToken()}`));

    ws.onopen = () => {
      resolve(ws);
    }

    ws.onclose = () => {
      reject("Disconnected");
    };
  });
}

export function disconnectFromWebSocket() {
  const ws = getWebSocket();
  
  if (ws) {
    ws.close();
    setWebSocket(null);
  }
}

export function sendChatMessage(message: string) {
  const ws = getWebSocket();

  if (ws) {
    ws.send(JSON.stringify({ opcode: 'chat', data: { text: message }}))
  }
}

export function getUserList(ws: WebSocket) {
  ws.send(JSON.stringify({ opcode: 'user_list' }));
}