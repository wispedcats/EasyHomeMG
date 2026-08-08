import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";

function App() {
  const path = window.location.pathname;

  if (path === "/") {
    return <Home />;
  }

  if (path === "/dashboard") {
    return <Dashboard />;
  }

  return <h1>404 Page not Found</h1>;
}

export default App;