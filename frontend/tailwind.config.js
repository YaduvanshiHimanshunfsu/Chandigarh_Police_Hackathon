/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        police: {
          navy: "#0a192f",
          dark: "#07111e",
          card: "#112240",
          accent: "#00d2ff",
          gold: "#e6af2e",
          danger: "#ff4d4d",
          success: "#00e676",
        },
      },
    },
  },
  plugins: [],
};
