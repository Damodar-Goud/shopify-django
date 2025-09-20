import RegisterPage from "./pages/RegisterPage";
import ProductsPage from "./pages/ProductsPage";
import LoginPage from "./pages/LoginPage";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </Router>
  );
}



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/products" element={<ProductsPage />} /> {/* ✅ New */}
      </Routes>
    </Router>
  );
}
