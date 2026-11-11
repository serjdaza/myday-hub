import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In dev, the browser talks only to Vite (port 5173). Requests to /api are
// forwarded to FastAPI, so the frontend code uses the same relative URLs
// ("/api/...") in dev and in prod (where FastAPI serves everything).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": process.env.VITE_API_PROXY ?? "http://localhost:8000",
    },
  },
});
