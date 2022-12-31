import { Component, createSignal, Match, onMount, Switch } from "solid-js";
import { useNavigate } from '@solidjs/router'
import { AiFillEye } from "../components/icons/AiFillEye";
import { AiFillEyeInvisible } from "../components/icons/AiFillEyeInvisible";
import { setAccessToken } from "../services/auth.service";
import { postLogin, postRegister } from "../services/ky.service";
import { OnSubmitEvent } from "./login.page";

export const RegisterPage: Component = () => {
  const navigate = useNavigate();
  const [login, setLogin] = createSignal("", { name: "login" });
  const [password, setPassword] = createSignal("", { name: "password" });
  const [passwordConfirm, setPasswordConfirm] = createSignal("", { name: "passwordConfirm" });
  const [isPasswordVisible, setIsPasswordVisible] = createSignal(false, {
    name: "IsPasswordVisible",
  });

  const handleSubmit = async (event: OnSubmitEvent) => {
    event.preventDefault();

    try {
      await postRegister({login: login(), password: password(), passwordConfirm: passwordConfirm()});
      const loginResponse = await postLogin({login: login(), password: password() });
      setAccessToken(loginResponse.access_token);
      navigate('/select');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div class="grid h-screen w-screen place-items-center">
      <form
        class="flex h-3/5 w-1/2 flex-col items-center justify-evenly gap-2 rounded-lg border-4 border-stone-600 bg-stone-200 p-8"
        onSubmit={handleSubmit}
      >
        <div>Logo</div>
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
          <div class="relative">
            <input
              class="w-full rounded-lg border-4 border-stone-600 p-2 indent-2 text-xl font-bold focus:border-lime-600 accent-lime-600"
              placeholder="Potwórz hasło"
              name="passwordConfirm"
              value={passwordConfirm()}
              onChange={(event) => setPasswordConfirm(event.currentTarget.value)}
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
        <button
          class="w-64 rounded-lg border-4 border-lime-900 bg-lime-500 py-2 text-xl font-bold text-lime-900 hover:text-lime-700 hover:border-lime-700"
          type="submit"
        >
          Zarejestruj się
        </button>
      </form>
    </div>
  )
}