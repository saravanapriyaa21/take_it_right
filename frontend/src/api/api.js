const BASE_URL = import.meta.env.VITE_API_URL;

console.log("Loaded API URL:", BASE_URL);

export async function analyzeMedicine(data) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || "Request failed");
  }

  return await response.json();
}
