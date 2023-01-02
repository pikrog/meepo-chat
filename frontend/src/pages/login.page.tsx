import { A, useNavigate } from "@solidjs/router";
import { Component, createSignal, Match, Show, Switch } from "solid-js";

import { AiFillEye } from "../components/icons/AiFillEye";
import { AiFillEyeInvisible } from "../components/icons/AiFillEyeInvisible";
import { postLogin } from "../services/fetch.service";

import MeepoChatLogo from '../../public/meepo-chat-logo.png';
import { Button } from "../components/Button";
import { setAccessToken } from "../services/auth.service";
import { setInLocalStorage } from "../services/local-storage.service";

export const LoginPage: Component = () => {
  const navigate = useNavigate();

  const [login, setLogin] = createSignal("", { name: "login" });
  const [password, setPassword] = createSignal("", { name: "password" });
  const [isPasswordVisible, setIsPasswordVisible] = createSignal(false, {
    name: "IsPasswordVisible",
  });

  const [error, setError] = createSignal("", { name: "error" });

  const handleSubmit = async (event: Event) => {
    event.preventDefault();

    try {
      const response = await postLogin({ login: login(), password: password() });
      setAccessToken(response.access_token);
      setInLocalStorage('access_token', response.access_token);
      navigate('/select');
    } catch (error: unknown) {
      console.error(error);
      if (typeof error === 'object' && 'detail' in error && typeof error.detail === 'string') {
        setError(error.detail);
      }
    }
  };

  return (
    <div class="grid h-screen w-screen place-items-center">
      <form
        onSubmit={handleSubmit}
        class="flex h-4/5 w-1/2 flex-col items-center justify-evenly gap-2 rounded-lg border-4 border-stone-600 bg-stone-200 p-8"
      >
        <img src={MeepoChatLogo} alt="Meepo Chat Logo" />
        <div class="flex w-full flex-col gap-2">
          <input
            required
            class="w-full rounded-lg border-4 border-stone-600 p-2 indent-2 text-xl font-bold focus:border-lime-600 accent-lime-600"
            placeholder="Login"
            id="login"
            name="login"
            type="text"
            minLength="3"
            onChange={(event) => setLogin(event.currentTarget.value)}
          />
          <div class="relative">
            <input
              required
              class="w-full rounded-lg border-4 border-stone-600 p-2 indent-2 text-xl font-bold focus:border-lime-600 accent-lime-600"
              minLength="6"
              placeholder="Hasło"
              name="password"
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
        <Button text="Zaloguj się" type="submit" />
        <A href="/register" class="text-lime-900 hover:text-lime-700">Nie masz konta? Zarejestruj się</A>
        <Show when={error().length > 0}>
          <div>
            <span class="text-red-600">{error()}</span>
          </div>
        </Show>
      </form>
    </div>
  );
};
