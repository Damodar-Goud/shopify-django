import { useEffect, useState } from "react";
import axios from "../api/axios";

function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get("/products/"); // ✅ Django API
        setProducts(response.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load products");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleAddToCart = async (productId) => {
    try {
      await axios.post("/orders/cart/add/", { product_id: productId, quantity: 1 });
      alert("✅ Added to cart!");
    } catch (err) {
      console.error(err);
      alert("❌ Failed to add to cart");
    }
  };

  if (loading) return <p className="text-center mt-10">Loading products...</p>;
  if (error) return <p className="text-center text-red-500 mt-10">{error}</p>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Products</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <div
            key={product.id}
            className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition"
          >
            <h2 className="text-lg font-semibold text-gray-700">{product.name}</h2>
            <p className="text-gray-500 text-sm mb-2">{product.description}</p>
            <p className="text-blue-600 font-bold mb-4">${product.price}</p>
            <button
              onClick={() => handleAddToCart(product.id)}
              className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700"
            >
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductsPage;
