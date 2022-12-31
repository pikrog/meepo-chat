import ky from "ky";

export const kyInstance = ky.create({ throwHttpErrors: true, prefixUrl: "http://localhost:3000/api/" });

type LoginDto = {
  login: string;
  password: string;
}

type LoginResponse = {
  access_token: string;
};

const at = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidXNlcm5hbWUiOiJKb2huIERvZSIsImlhdCI6MTUxNjIzOTAyMn0.sfyvsYjhR81buXRDvU0MS_m2kfwXTfXvclVM0-3F-GQ'

export const postLogin = async (loginDto: LoginDto) => {
  // const response = await ky.post("auth/login", {
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
  const response = await ky.post("auth/register", {
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
  const response = await ky.get("/servers");

  return response.json<GetServer[]>();
};
