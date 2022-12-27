import ky from "ky";

export const kyInstance = ky.create({ throwHttpErrors: true });

export const kyLogin = async (login: string, password: string) => {
  const response = await ky.post("http://localhost:3000/api/auth/login", {
    body: JSON.stringify({ login, password }),
  });
  return true;
};
