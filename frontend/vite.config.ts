import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'

function getBackendPort() {
  if (process.env.PORT) return process.env.PORT;
  if (process.env.BACKEND_PORT) return process.env.BACKEND_PORT;

  try {
    const envPath = path.resolve(process.cwd(), '../.env');
    if (fs.existsSync(envPath)) {
      const content = fs.readFileSync(envPath, 'utf-8');
      const lines = content.split('\n');
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
          const [key, ...valueParts] = trimmed.split('=');
          if (key.trim() === 'PORT') {
            return valueParts.join('=').trim().replace(/^['"]|['"]$/g, '');
          }
        }
      }
    }
  } catch (e) {
    console.error('Error reading root .env file:', e);
  }
  return '8000';
}

const backendPort = getBackendPort();

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: `http://127.0.0.1:${backendPort}`,
        changeOrigin: true,
        secure: false
      }
    }
  }
})
