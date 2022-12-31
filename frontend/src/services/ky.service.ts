import ky from "ky";

export const kyInstance = ky.create({ throwHttpErrors: true, credentials: 'include' });

type LoginDto = {
  login: string;
  password: string;
}

type LoginResponse = {
  access_token: string;
};

const at = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3MjIyIiwidXNlcm5hbWUiOiJKb2FzZERvZSIsInVzZXJfaWQiOjEyLCJ1c2VyX25hbWUiOiJ0ZXN0IiwiaWF0IjoxNTE2MjM5MDIyLCJpc3MiOiJtYXN0ZXItc2VydmVyIn0.kuQ7AMYug7u0b_DwNLSfFL-VVIw2Vy7NOpx3V34whXQ'

export const postLogin = async (loginDto: LoginDto) => {
  // const response = await ky.post("http://localhost:3000/api/auth/login", {
  //   body: JSON.stringify(loginDto),
  // });


  return { access_token: at };
  // return response.json<LoginResponse>();
};

type RegisterDto = {
  login: string;
  password: string;
  passwordConfirm: string;
};

type RegisterResponse = {
  userId: number;
  login: string;
};

export const postRegister = async (registerDto: RegisterDto) => {
  const response = await ky.post("http://localhost:3000/api/auth/register", {
    body: JSON.stringify(registerDto)
  });

  return response.json<RegisterResponse>()
};

export type GetServer = {
  serverId: number;
  address: string;
  name: string;
};

export const getServers = async () => {
  const response = await ky.get("http://localhost:3000/api/servers");

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
  document.cookie = `access_token=${at}`;
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
