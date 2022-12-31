import { A, useNavigate } from "@solidjs/router";
import { Component, createSignal, Match, Switch } from "solid-js";

import { AiFillEye } from "../components/icons/AiFillEye";
import { AiFillEyeInvisible } from "../components/icons/AiFillEyeInvisible";
import { postLogin } from "../services/ky.service";

import MeepoChatLogo from '../../public/meepo-chat-logo.png';
import { Button } from "../components/Button";
import { setAccessToken } from "../services/auth.service";

export const LoginPage: Component = () => {
  const navigate = useNavigate();

  const [login, setLogin] = createSignal("", { name: "login" });
  const [password, setPassword] = createSignal("", { name: "password" });
  const [isPasswordVisible, setIsPasswordVisible] = createSignal(false, {
    name: "IsPasswordVisible",
  });

  const handleSubmit = async (event: MouseEvent) => {
    event.preventDefault();
    const response = await postLogin({ login: login(), password: password() });
    setAccessToken(response.access_token);
    navigate('/select');
  };

  return (
    <div class="grid h-screen w-screen place-items-center">
      <form
        class="flex h-4/5 w-1/2 flex-col items-center justify-evenly gap-2 rounded-lg border-4 border-stone-600 bg-stone-200 p-8"
      >
        <img src={MeepoChatLogo} alt="Meepo Chat Logo" />
        <div class="flex w-full flex-col gap-2">
          <input
            class="w-full rounded-lg border-4 border-stone-600 p-2 indent-2 text-xl font-bold focus:border-lime-600 accent-lime-600"
            placeholder="Login"
            name="login"
            type="text"
            value={login()}
            onChange={(event) => setLogin(event.currentTarget.value)}
          />
          <div class="relative">
            <input
              class="w-full rounded-lg border-4 border-stone-600 p-2 indent-2 text-xl font-bold focus:border-lime-600 accent-lime-600"
              placeholder="Hasło"
              name="password"
              value={password()}
              onChange={(event) => setPassword(event.currentTarget.value)}
              type={isPasswordVisible() ? "text" : "password"}
            />
            <div
              class="absolute top-2.5 right-4 cursor-pointer"
              onClick={() => setIsPasswordVisible((prev) => !prev)}
            >
              <Switch>
                <Match when={isPasswordVisible() === true}>
                  <AiFillEye width="2em" height="2em" />
                </Match>
                <Match when={isPasswordVisible() === false}>
                  <AiFillEyeInvisible width="2em" height="2em" />
                </Match>
              </Switch>
            </div>
          </div>
        </div>
        <Button text="Zaloguj się" onClick={handleSubmit} />
        <A href="/register" class="text-lime-900 hover:text-lime-700">Nie masz konta? Zarejestruj się</A>
      </form>
    </div>
  );
};
