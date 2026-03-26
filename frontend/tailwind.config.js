/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "Space Grotesk",
          "Sora",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
        display: ["Sora", "Space Grotesk", "system-ui", "sans-serif"],
      },
      colors: {
        brand: {
          50: "#eefef8",
          100: "#d6fcef",
          200: "#adf8df",
          300: "#7bf0ca",
          400: "#40e1b1",
          500: "#18c69a",
          600: "#0e9f7e",
          700: "#0e7f66",
          800: "#116352",
          900: "#115244",
        },
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
