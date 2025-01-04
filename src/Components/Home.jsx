import React from "react";
import dashboard from "../assets/dashboard.png";
import traffic_lights from "../assets/traffic-lights.png";
import traffic_controls from "../assets/traffic-control.png";

const Home = () => {
    return (
        <div className="  mt-8">
            <h1 className="text-4xl text-center uppercase font-black text-[#c0c0c0] ">
                "Your one-stop solution for real-time traffic issues"
            </h1>
            <div className="px-20 mt-16  border-[#c0c0c0]">
                <h1 className="text-3xl text-[#c0c0c0] font-extrabold">
                    Our Features
                </h1>
                <div className="cards flex justify-evenly gap-10 mt-10 ">
                    <div className="card mb-14 flex flex-col items-center w-1/3  rounded-lg p-4 mt-4">
                        <img
                            src={traffic_controls}
                            alt=""
                            className="w-20 h-20 "
                        />
                        <p className="text-2xl font-bold text-[#c0c0c0] mt-5">
                            Traffic Management
                        </p>
                    </div>
                    <div className="card  mb-14 flex flex-col items-center w-1/3  rounded-lg p-4 mt-4">
                        <img
                            src={traffic_lights}
                            alt=""
                            className="w-20 h-20 "
                        />
                        <p className="text-2xl font-bold text-[#c0c0c0] mt-5">
                            Traffic Prediction
                        </p>
                    </div>
                    <div className="card  mb-14 flex flex-col items-center w-1/3  rounded-lg p-4 mt-4">
                        <img
                            src={dashboard}
                            alt=""
                            className="w-20 h-20 "
                        />
                        <p className="text-2xl font-bold text-[#c0c0c0] mt-5">
                            Real-time Dashboard
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
