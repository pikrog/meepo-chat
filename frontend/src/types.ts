import type { JSX } from "solid-js";

export type Message = {
  id: number;
  content: string;
  user: {
    id: number;
    name: string;
  };
  timestamp: Date;
};

export type User = {
  id: number;
  name: string;
};

export type OnKeyPress = JSX.EventHandlerUnion<
  HTMLTextAreaElement,
  KeyboardEvent
>;

export type OnDivClick = JSX.EventHandlerUnion<HTMLDivElement, PointerEvent>;
export type OnButtonClick = JSX.EventHandlerUnion<
  HTMLButtonElement,
  PointerEvent
>;

export type OnInput = JSX.EventHandlerUnion<HTMLTextAreaElement, InputEvent>;

export type Ref<T> = T | null;

export type JoinChatMessage = {
  opcode: 'chat';
  data: {
    sender: string;
    timestamp: string;
    type: 'join';
  };
}

export type TextChatMessage = {
  opcode: 'chat';
  data: {
    sender: string;
    timestamp: string;
    text: string;
    type: 'chat';
  };
}

export type LeaveChatMessage = {
  opcode: 'chat';
  data: {
    sender: string;
    timestamp: string;
    type: 'leave';
  };
}

export type UserListMessage = {
  opcode: 'user_list';
  data: {
    name: string;
  }[];
}

export type ErrorMessage = {
  opcode: 'error';
  data: string;
}

export type MessageMessageChat = {
  id: string;
  type: 'chat';
  sender: string;
  sender_id: number;
  timestamp: string;
  text: string;
}

type MessageMessageOther = {
  id: string;
  type: 'join' | 'leave';
  sender: string;
  sender_id: number;
  timestamp: string;
  text: null;
}

export type MessagesMessage = {
  opcode: 'messages';
  data: (MessageMessageChat | MessageMessageOther)[];
}

export type WSMessage = JoinChatMessage | TextChatMessage | LeaveChatMessage | UserListMessage | ErrorMessage | MessagesMessage;
export type ChatMessage = JoinChatMessage | TextChatMessage | LeaveChatMessage;
