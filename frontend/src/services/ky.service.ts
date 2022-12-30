import ky from "ky";

export const kyInstance = ky.create({ throwHttpErrors: true, prefixUrl: "http://localhost:3000/api/" });

type LoginDto = {
  login: string;
  password: string;
}

export const kyLogin = async (loginDto: LoginDto) => {
  await ky.post("auth/login", {
    body: JSON.stringify(loginDto),
  });
  return true;
};

type RegisterDto = {
  login: string;
  password: string;
  passwordConfirm: string;
};

export const postRegister = async (registerDto: RegisterDto) => {
  await ky.post("auth/register", {
    body: JSON.stringify(registerDto)
  })

  return true;
};
