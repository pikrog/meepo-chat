import { json } from "solid-start";

export function GET() {
  console.log(process.env);
  return json({ url: process.env.VITE_MASTER ?? import.meta.env.VITE_MASTER }); 
}