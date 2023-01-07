import { useNavigate } from "solid-start";
import { onMount } from "solid-js";
import { getFromLocalStorage } from "../services/local-storage.service";

export default function Home() {
  const navigate = useNavigate();

  onMount(() => {
    navigate((getFromLocalStorage('access_token') ?? '').length > 0 ? "/select" : "/login");
  })

  return (
    <></>
  );
}
