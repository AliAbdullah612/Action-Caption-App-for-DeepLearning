"use client";

import { useState } from "react";

export default function Home() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [action, setAction] = useState("");
  const [caption, setCaption] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const sendImage = async () => {
    if (!image) {
      alert("Please select an image");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setAction(data.action);
      setCaption(data.caption);
    } catch (error) {
      alert("Backend not responding");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Action Recognition & Captioning</h1>

      <input type="file" accept="image/*" onChange={handleImageChange} />

      {preview && <img src={preview} className="image" />}

      <button onClick={sendImage}>
        {loading ? "Processing..." : "Recognize Action"}
      </button>

      {action && (
        <div className="result">
          <p><b>Action:</b> {action}</p>
          <p><b>Caption:</b> {caption}</p>
        </div>
      )}
    </div>
  );
}
