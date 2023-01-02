import { Component, onMount } from "solid-js";
import { Routes, Route, useNavigate } from "@solidjs/router";
import { LoginPage } from "../pages/login.page";
import { ChatPage } from "../pages/chat.page";
import { RegisterPage } from "../pages/register.page";
import { SelectPage } from "../pages/select.page";
import { getAccessToken } from "../services/auth.service";

export const RouterProvider: Component = () => {
  const navigate = useNavigate();

  onMount(() => {
    if (location.pathname === '/') {
      if (getAccessToken().length > 0) {
        navigate('/select');
      } 
    }
    
    if (getAccessToken().length === 0) {
      navigate('/login');
    }
  });

  return (
    <Routes>
      <Route path={"/chat"} component={ChatPage} />
      <Route path={"/login"} component={LoginPage} />
      <Route path={"/register"} component={RegisterPage} />
      <Route path={"/select"} component={SelectPage} />
    </Routes>
  );
};
