import ky from "ky";

export const kyInstance = ky.create({ throwHttpErrors: true, credentials: 'include' });

type LoginDto = {
  login: string;
  password: string;
}

type LoginResponse = {
  access_token: string;
};

const at = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODIyIiwidXNlcm5hbWUiOiJKb2huIERvZSIsImlhdCI6MTUxNjIzOTAyMiwiaXNzIjoibWFzdGVyLXNlcnZlciJ9.QMKz4ypMo9cIDhmIsNkzhVlrSQc0y-a-SB1xYITuCR0'

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

    console.log('my');
    const response = await ky.get(`http://${serverAddress}/api/chat/messages`,
    {
      throwHttpErrors: false,
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      credentials: 'include',
    });
    // const res = await fetch(`http://${serverAddress}/api/chat/messages`, { credentials: 'include' })
    // console.log('my', response, res);
    console.log('end', response);
    return response.json<ReponseMessage[]>();
  } catch(error) {
    console.error(error);
  };
};
