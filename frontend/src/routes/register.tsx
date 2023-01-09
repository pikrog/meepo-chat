import { createSignal, Match, onMount, Show, Switch } from "solid-js";
import { AiFillEye } from "~/components/AiFillEye";
import { AiFillEyeInvisible } from "~/components/AiFillEyeInvisible";
import { redirectToSelectIfLoggedIn, setAccessToken } from "../services/auth.service";
import { postLogin, postRegister } from "../services/fetch.service";

import MeepoChatLogo from '../../public/meepo-chat-logo.png';
import { Button } from "../components/Button";
import { useNavigate } from "solid-start";
import { setInLocalStorage } from "../services/local-storage.service";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [login, setLogin] = createSignal("", { name: "login" });
  const [password, setPassword] = createSignal("", { name: "password" });
  const [passwordConfirm, setPasswordConfirm] = createSignal("", { name: "passwordConfirm" });
  const [isPasswordVisible, setIsPasswordVisible] = createSignal(false, {
    name: "IsPasswordVisible",
  });

  const [error, setError] = createSignal("", { name: "error" });

  const handleSubmit = async (event: Event) => {
    event.preventDefault();

    try {
      await postRegister({login: login(), password: password(), pass_comp: passwordConfirm()});
      const loginResponse = await postLogin({login: login(), password: password() });
      setAccessToken(loginResponse.access_token);
      setInLocalStorage('access_token', loginResponse.access_token);
      navigate('/select');
    } catch (error: unknown) {
      console.error(error);
      if (typeof error === 'object' && error && 'detail' in error && typeof error.detail === 'string') {
        if (error.detail === 'Passwords do not match') {
          setError("Hasła nie są identyczne");
        } else if (error.detail === 'This user name is already taken') {
          setError("Istnieje już użytkownik o takim loginie");
        } else {
          setError(error.detail);
        }
      } else {
        setError("Wystąpił nieoczekiwany błąd");
      }
    }
  };

  onMount(() => {
    redirectToSelectIfLoggedIn(navigate);
  })

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
            name="login"
            type="text"
            minLength="3"
            onChange={(event) => setLogin(event.currentTarget.value)}
          />
          <div class="relative">
            <input
              required
              class="w-full rounded-lg border-4 border-stone-600 p-2 indent-2 text-xl font-bold focus:border-lime-600 accent-lime-600"
              placeholder="Hasło"
              name="password"
              minLength="6"
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
              required
              class="w-full rounded-lg border-4 border-stone-600 p-2 indent-2 text-xl font-bold focus:border-lime-600 accent-lime-600"
              placeholder="Potwórz hasło"
              name="passwordConfirm"
              minLength="6"
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
        <Button
          type="submit"
          text="Zarejestruj się"
        />
        <Show when={error().length > 0}>
          <div>
            <span class="text-red-600">{error()}</span>
          </div>
        </Show>
      </form>
    </div>
  )
}