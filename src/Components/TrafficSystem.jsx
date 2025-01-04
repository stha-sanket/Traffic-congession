import React from "react";
import Navbar from "./Navbar";

const TrafficSystem = () => {
    return (
        <div className="traffic_system h-screen ">
            <Navbar />
            <div className="flex justify-center h-full flex-col items-center">
                <div className="webcam flex justify-center items-center mt-[-150px] w-1/2 h-1/2 rounded-lg mx-20 border border-[#c0c0c0]">
                    <p>Webcam</p>
                </div>
            <div className="button flex justify-center gap-10 mt-10">
                <button className="w-64 border p-5 rounded-lg text-2xl font-medium text-[#101010] bg-[#ff7f11] "> Open Cam</button>
                <button className="w-64 border p-5 rounded-lg text-2xl font-medium text-[#101010] bg-red-600"> Stop </button>
                <button className="w-64 border p-5 rounded-lg text-2xl font-medium text-[#101010] bg-[#00aeef] "> Upload</button>
            </div>
            </div>
            <div className="time">
                <div className="cards flex justify-evenly gap-10 mx-10 ">
                    <div className="card mb-14 flex flex-col border border-[#c0c0c0] items-center w-1/3  rounded-lg p-4 mt-4">
                    <p className="text-xl text-[#c0c0c0] font-semibold">Current Traffic</p>
                    <p className="text-4xl text-[#c0c0c0] font-bold">Highly Congested</p>
                    </div>

                </div>
            </div>

            <div className="flex justify-center h-full  flex-col items-center">
                <div className="webcam flex justify-center items-center mt-[-150px] w-1/2 h-1/2 rounded-lg mx-20 border border-[#c0c0c0]">
                    <p>Webcam</p>
                </div>
            </div>
        </div>
    );
};

export default TrafficSystem;
