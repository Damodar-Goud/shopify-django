const [email, setEmail] = useState("");
const [password, setPassword] = useState("");

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await axios.post("/auth/login/", {
  username: email,   // 👈 send email inside username field
  password,
});


    // Save token
    localStorage.setItem("token", response.data.access);

    // Redirect to products page
    navigate("/products");
  } catch (err) {
    console.error(err.response?.data || err.message);
    setError(err.response?.data?.detail || "Invalid credentials");
  }
};
