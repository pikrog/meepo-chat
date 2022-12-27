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
