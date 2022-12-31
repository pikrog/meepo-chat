import { Component } from "solid-js"

export const Button: Component<{
  onClick: (event?: MouseEvent) => void;
  text: string;
  disabled?: boolean;
}> = (props) => {
  return (
    <button 
      class={`h-16 w-64 px-2 rounded-lg border-4 border-lime-900 font-bold text-xl ${
        props.disabled ? 'border-stone-400 bg-stone-300 text-stone-400' : 'text-lime-900 hover:text-lime-700 bg-lime-500 hover:brightness-105'
      }`}
      onClick={props.onClick}
      disabled={props.disabled}
    >
      {props.text}
    </button>
  )
}