import Temperature from "./widgets/Temperature"
import "./css/Hero.css"

export default function Hero() {
    return (
        <section className="relative flex min-h-screen flex-col items-center justify-center gap-8">

            <button className="Btn-Container">
                <span className="btn-text">Dashboard</span>

                <span className="icon-Container">
                    <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                    >
                        <path
                            d="M5 12H19M19 12L13 6M19 12L13 18"
                            stroke="white"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                </span>
            </button>

            <Temperature />

        </section>
    )
}