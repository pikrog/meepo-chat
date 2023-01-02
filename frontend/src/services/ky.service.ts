import ky from "ky";
import { constants } from "../lib/constants";
import { getAccessToken } from "./auth.service";

export const kyInstance = ky.create({
  throwHttpErrors: true,
  // mode: 'cors',
  // headers: {
  //   'Access-Control-Allow-Origin': '*',
  //   // 'Content-Type': 'application/json'
  // },
  // credentials: 'include'
});

type LoginDto = {
  login: string;
  password: string;
}

type LoginResponse = {
  access_token: string;
};

export const postLogin = async (loginDto: LoginDto) => {
  const response = await fetch(`${constants.masterServerUrl}/login`, {
    method: 'POST',
    body: JSON.stringify(loginDto),
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    }
  })

  const json = await response.json() as LoginResponse;
  document.cookie = `access_token=${json.access_token}`;
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
  const response = await ky.post(`${constants.masterServerUrl}/register`, {
    json: registerDto
  });

  return response.json<RegisterResponse>()
};

export type GetServer = {
  address: string;
  name: string;
  last_heartbeat: string;
};

export const getServers = async () => {
  const response = await ky.get(`${constants.masterServerUrl}/servers`);

  return response.json<GetServer[]>();
};

type ReponseMessage = {
  id: string;
  type: 'join' | 'leave' | 'chat';
  sender: string;
  timestamp: string;
  text: null | string;
}

export const getServerMessage = async (serverAddress: string) => {
  try {
    const response = await ky.get(`http://${serverAddress}/api/chat/messages`,
    {
      throwHttpErrors: false,
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      credentials: 'include',
    });
    return response.json<ReponseMessage[]>();
  } catch(error) {
    console.error(error);
  };
};
