import { createRouteData, useNavigate, useRouteData } from "solid-start";
import { config } from 'dotenv';
import { setMasterServerUrl } from "../services/fetch.service";
import { onMount } from "solid-js";
import { getFromLocalStorage } from "../services/local-storage.service";

export function routeData() {
  return createRouteData(() => {
    const result = config()
    return result.parsed?.VITE_MASTER ?? process.env.VITE_MASTER ?? '';
  });
}

export default function Home() {
  const navigate = useNavigate();

  const data = useRouteData<typeof routeData>();
  setMasterServerUrl(data() ?? '');

  onMount(() => {
    navigate((getFromLocalStorage('access_token') ?? '').length > 0 ? "/select" : "/login");
  })

  return (
    <></>
  );
}
