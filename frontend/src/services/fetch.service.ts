import { createSignal } from "solid-js";

export const [masterServerUrl, setMasterServerUrl] = createSignal('', {
  name: 'masterServerUrl'
})

type LoginDto = {
  login: string;
  password: string;
}

type LoginResponse = {
  access_token: string;
};

export const postLogin = async (loginDto: LoginDto) => {
  const response = await fetch(`${masterServerUrl()}/login`, {
    method: 'POST',
    body: JSON.stringify(loginDto),
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    }
  });

  if (!response.ok) {
    throw await response.json();
  }

  const json = await response.json() as LoginResponse;
  return json;
};

type RegisterDto = {
  login: string;
  password: string;
  pass_comp: string;
};

type RegisterResponse = {
  userId: number;
  login: string;
};

export const postRegister = async (registerDto: RegisterDto) => {
  const response = await fetch(`${masterServerUrl()}/register`, {
    body: JSON.stringify(registerDto),
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    }
  });

  if (!response.ok) {
    throw await response.json();
  }

  return await response.json() as RegisterResponse;
};

export type GetServer = {
  address: string;
  name: string;
  last_heartbeat: string;
};

export const getServers = async () => {
  const response = await fetch(`${masterServerUrl()}/servers`, {
    mode: 'cors',
  });

  if (!response.ok) {
    throw await response.json();
  }

  return await response.json() as GetServer[];
};

type ReponseMessage = {
  id: string;
  type: 'join' | 'leave' | 'chat';
  sender: string;
  timestamp: string;
  text: null | string;
}

export const getServerMessage = async (serverAddress: string) => {
  const response = await fetch(`http://${serverAddress}/api/chat/messages`,
    {
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      credentials: 'include',
    }
  );

  if (!response.ok) {
    throw await response.json();
  }

  return await response.json() as ReponseMessage[];
};

export type ServerInfo = {
  server_name: string;
  num_clients: number;
  max_clients: number;
};

export const getServerInfo = async (serverAddress: string) => {
  const response = await fetch(`http://${serverAddress}/api/server/info`,
    {
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      credentials: 'include',
    }
  );

  if (!response.ok) {
    throw await response.json();
  }

  return await response.json() as ServerInfo;
}

export type FullServerInfo = ServerInfo & GetServer;