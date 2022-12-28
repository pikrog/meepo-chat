import { Component } from "solid-js";
import { Router, Routes, Route } from "@solidjs/router";
import { LoginPage } from "../pages/login.page";
import { ChatPage } from "../pages/chat.page";
import { RegisterPage } from "../pages/register.page";

export const RouterProvider: Component = () => {
  return (
    <Router>
      <Routes>
        <Route path={"/chat"} component={ChatPage} />
        <Route path={"/login"} component={LoginPage} />
        <Route path={"/register"} component={RegisterPage} />
      </Routes>
    </Router>
  );
};
