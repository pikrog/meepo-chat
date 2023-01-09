// @refresh reload
import { onMount, Suspense } from "solid-js";
import {
  Body,
  ErrorBoundary,
  FileRoutes,
  Head,
  Html,
  Meta,
  Routes,
  Scripts,
  Title,
} from "solid-start";
import "./root.css";
import { setAccessToken } from "./services/auth.service";
import { setServerAddress } from "./services/chat.service";
import { setMasterServerUrl } from "./services/fetch.service";
import { getFromLocalStorage } from "./services/local-storage.service";

export default function Root() {
  if (typeof window !== 'undefined') {
    setAccessToken(getFromLocalStorage('access_token') ?? '');
    setServerAddress(getFromLocalStorage('server_address') ?? '');
  }

  onMount(async () => {
    const response = await fetch(`${location.origin}/api/master`);
    const json = await response.json();
    setMasterServerUrl(json.url);
  })

  return (
    <Html lang="pl">
      <Head>
        <Title>Meepo Chat</Title>
        <Meta charset="utf-8" />
        <Meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Body>
        <Suspense>
          <ErrorBoundary>
            <Routes>
              <FileRoutes />
            </Routes>
          </ErrorBoundary>
        </Suspense>
        <Scripts />
      </Body>
    </Html>
  );
}
