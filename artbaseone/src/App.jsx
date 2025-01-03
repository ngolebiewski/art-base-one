import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [titles, setTitles] = useState([]); // State to store artwork titles
  const [error, setError] = useState(null); // State to store any errors
  const [artworks, setArtworks] = useState([]);
  const apiUrl = import.meta.env.VITE_API_URL || "/api";  // Use environment variable or fallback to relative API path

  useEffect(() => {
    const fetchTitles = async () => {
      try {
        const response = await axios.get(`${apiUrl}/artworks/titles`);
        setTitles(response.data.titles); // Assuming the response contains a `titles` array
      } catch (err) {
        setError("Failed to load artwork titles");
        console.error(err);
      }
    };

    const fetchArtworks = async () => {
      try {
        const { data } = await axios.get(`${apiUrl}/artworks/all`);
        console.log(data.data);
        setArtworks(data.data);
      } catch (err) {
        setError("Failed to load artworks");
        console.error(err);
      }
    };

    fetchTitles();
    fetchArtworks();
  }, []);


  return (
    <>
      <h1>Art Base One</h1>
      {error && <p style={{ color: "red" }}>{error}</p>} {/* Display error message */}
      {titles.length > 0 ? (
        <ul>
          {titles.map((title, index) => (
            <li key={index}>{title}</li>
          ))}
        </ul>
      ) : (
        <p>Loading titles...</p>
      )}



<h1>Artworks</h1>
      {artworks.length > 0 ? (
        <ul>
          {artworks.map((artwork, index) => (
            <li key={index}>
              <h3>{artwork.title}</h3>
              <img
                src={artwork.image_url}
                alt={artwork.title}
                style={{ maxWidth: "200px", height: "auto" }}
              />
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading artworks...</p>
      )}
    </>
  );



}

export default App;
