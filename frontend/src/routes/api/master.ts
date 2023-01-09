import { json } from "solid-start";

export function GET() {
  return json({ url: process.env.VITE_MASTER }); 
}