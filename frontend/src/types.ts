export type Message = {
  id: number;
  text: string;
  user: {
    id: number;
    name: string;
  };
  timestamp: string;
};