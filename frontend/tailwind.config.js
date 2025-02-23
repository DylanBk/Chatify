/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "offBlack": "#333",
        "grey--000": "#FAF9F6",
        "grey--100": "#eee",
        "grey--200": "#ddd",
        "grey--300": "#d9d9d9",
        "red--100": "#D22B2B",
        "red--200": "#b11a1a",
        "blue--100": "#6495ED",
        "blue--200": "#3455cd",
        "blue--300": "#6495ed33",
      }
    },
  },
  plugins: [],
}