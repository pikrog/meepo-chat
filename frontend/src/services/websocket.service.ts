import { Accessor, createSignal, Setter } from "solid-js";
import { ChatMessage, MessageMessageChat, TextChatMessage, WSMessage } from "../types";
import { getAccessToken } from "./auth.service";

type ChatServerWebSocketOptions = {
  onClose?: (closeEvent: CloseEvent) => void;
  onChatMessage?: (chatMessage: ChatMessage) => void;
  onMessage?: (message: WSMessage) => void;
  onError?: (event: Event) => void;
  onOpen?: (event: Event) => void;
  onMessages?: () => void;
}

export const [getMessages, setMessages] = createSignal<ChatMessage[]>([]);
export const [getUserList, setUserList] = createSignal<string[]>([]);
export const [getWSError, setWSError] = createSignal('');
export const [shouldReconnect, setShouldReconnect] = createSignal(true);

export class ChatServerWebSocket {
  public readonly chatServerUrl: string;
  public readonly websocket: WebSocket;
  public readonly options?: ChatServerWebSocketOptions;

  public readonly getMessages: Accessor<ChatMessage[]>;
  public readonly getUserList: Accessor<string[]>;
  
  private readonly setMessages: Setter<ChatMessage[]>;
  private readonly setUserList: Setter<string[]>;

  constructor(chatServerUrl: string, options?: ChatServerWebSocketOptions) {
    this.getMessages = getMessages;
    this.setMessages = setMessages;

    this.getUserList = getUserList;
    this.setUserList = setUserList;

    this.chatServerUrl = chatServerUrl;
    this.options = options;

    this.websocket = new WebSocket(`ws://${chatServerUrl}/ws`);
    this.websocket.onopen = this.handleOpen.bind(this);
    this.websocket.onmessage = this.handleMessage.bind(this);
    this.websocket.onerror = this.handleError.bind(this);
    this.websocket.onclose = this.handleClose.bind(this);
  }

  handleOpen(event: Event) {
    console.info(`[CHAT] (${this.chatServerUrl}) Opening WS`);
    setShouldReconnect(true);
    this.authenticate();
    
    this.options?.onOpen?.(event);
  }

  handleMessage(event: MessageEvent<string>) {
    console.info(`[CHAT] (${this.chatServerUrl}) Received message`);

    const message = JSON.parse(event.data) as WSMessage;

    if (message.opcode === 'chat') {
      this.setMessages((prev) => prev.concat([message]));

      if (message.data.type === 'leave') {
        this.setUserList((prev) => prev.filter((name) => name !== message.data.sender));
      } else if (message.data.type === 'join') {
        this.setUserList((prev) => prev.concat([message.data.sender]));
      }

      this.options?.onChatMessage?.(message);
    } else if (message.opcode === 'user_list') {
      this.setUserList(message.data.map((user) => user.name));
    } else if (message.opcode === 'messages') {
      const filteredMessages = message.data
        .filter((item) => item.type === 'chat')
        .map((item) => {
          const msg = item as MessageMessageChat;
          return {
            opcode: 'chat' as const,
            data: {
              sender: msg.sender,
              text: msg.text,
              timestamp: msg.timestamp,
              type: msg.type
            }
          }
        })
        .sort((a, b) => a.data.timestamp > b.data.timestamp ? 1 : -1)

      this.setMessages(filteredMessages);

      this.options?.onMessages?.();
    } else if (message.opcode === 'error') {
      if (message.data === 'the user is already in the room') {
        setWSError('Użytkownik o podanym loginie znajduje się już w tym pokoju');
        setShouldReconnect(false);
      } else if (message.data === 'the chat room is full') {
        setWSError('Pokój jest pełny');
        setShouldReconnect(false);
      } else if (message.data === 'credentials expired') {
        setWSError('Dane logowania wygasły');
        setShouldReconnect(false);
      } else if (message.data === 'no credentials were provided') {
        setWSError('Błąd danych logowania');
        setShouldReconnect(false);
      } else {
        setWSError('Nieznany błąd');
      }
    }

    this.options?.onMessage?.(message);
  }

  handleError(error: Event) {
    console.info(`[CHAT] (${this.chatServerUrl}) Error ${error.type}`);

    this.options?.onError?.(error);
  }

  handleClose(event: CloseEvent) {
    console.info(`[CHAT] (${this.chatServerUrl}) Closing WS`);
    this.options?.onClose?.(event);
  }

  closeWebSocket() {
    this.websocket.close();
  }

  getOnlyTextMessages() {
    return this.getMessages().filter((message) => message.data.type === 'chat');
  }

  authenticate() {
    this.websocket.send(JSON.stringify({ opcode: 'auth', data: getAccessToken() }));
  }

  fetchMessages(count?: number) {
    this.websocket.send(JSON.stringify({ opcode: 'messages', data: { start_id: null, count: count ?? 100 }}));
  }

  fetchUserList() {
    this.websocket.send(JSON.stringify({ opcode: 'user_list' }));
  }

  postChatMessage(content: string) {
    this.websocket.send(JSON.stringify({ opcode: 'chat', data: { text: content }}))
  }

  cleanUserList() {
    setUserList([]);
  }
  
  cleanMessages() {
    setMessages([]);
  }
}