// Tailwind v3 — compilado pelo executável standalone (sem Node):
//   tailwindcss -i assets/tailwind.css -o core/static/core/css/site.css --minify
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        // Cor de destaque única ("run green", da skill ui-ux-pro-max)
        accent: {
          300: "#86efac",
          400: "#4ade80",
          500: "#22c55e",
          600: "#16a34a",
        },
        // Tons de fundo e bordas (paleta Dark Mode da skill; combina com o azul do logo)
        surface: {
          950: "#0F172A",
          900: "#1B2336",
          800: "#222B3F",
          700: "#272F42",
          600: "#475569",
        },
      },
      fontFamily: {
        sans: ["'IBM Plex Sans'", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
