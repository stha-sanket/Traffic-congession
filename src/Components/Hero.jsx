import React from "react";
import Navbar from "./Navbar";
import hero from "../assets/hero.mp4";
import Home from "./Home";

const Hero = () => {
    return (
      <>
        <div className="h-screen ">
            <Navbar />
            <div className="hero w-full absolute">
                <div className="relative w-full h-screen overflow-hidden mt-[-80px]">
                    {/* Background video */}
                    <video
                        className="absolute top-0 left-0 w-full h-full object-cover"
                        src={hero}
                        autoPlay
                        muted
                        loop
                    />
                    {/* Overlay content */}
                    <div className="relative z-1 flex flex-col justify-center pl-20 h-full text-white bg-black bg-opacity-50">
                        <h1 className="text-4xl font-bold md:text-6xl text-[#c0c0c0] ">
                            Navigate Smarter
                        </h1>
                        <p className="mt-4 text-lg md:text-xl font-bold text-[#c0c0c0]">
                            Travel easier
                        </p>
                    </div>
                </div>

            </div>
        </div>
        <Home />
        </>
    );
};

export default Hero;
