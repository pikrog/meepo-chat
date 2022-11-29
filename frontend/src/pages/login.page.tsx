import { Component, createSignal, type JSX } from "solid-js";

export const LoginPage: Component = () => {
  const [isPasswordVisible, setIsPasswordVisible] = createSignal(false, { name: "IsPasswordVisible" });

  return (
    <div class="h-screen w-screen">
      <form class="flex flex-col" onSubmit={(event) => {
        event.preventDefault();

        
      }}>
        <div>Logo</div>
        <input type="text" />
        <input type={isPasswordVisible ? "text" : "password"} />
        <button type="submit">Zaloguj się</button>
      </form>
    </div>
  );
}