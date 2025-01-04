import React from "react";
import Navbar from "./Navbar";

const Analytic = () => {
    return (
        <div>
            <Navbar />
            <div className="time">
                <div className="cards flex justify-evenly gap-10 mt-10 mx-10 ">
                    <div className="card mb-14 flex flex-col border border-[#c0c0c0] items-center w-1/3  rounded-lg p-4 mt-4">
                    <p className="text-xl text-[#c0c0c0] font-semibold">Estimated Peak Hour Today</p>
                    <p className="text-4xl text-[#c0c0c0] font-bold">5:00 PM</p>
                    </div>
                    <div className="card  mb-14 flex flex-col border border-[#c0c0c0] items-center w-1/3  rounded-lg p-4 mt-4">
                    <p className="text-xl text-[#c0c0c0] font-semibold">Estimated Peak Day</p>
                    <p className="text-4xl text-[#c0c0c0] font-bold">Saturday</p>
                    </div>
                </div>
            </div>

            <div className="traffic_trend hourly">
                <div className="chart px-20">
                    <h1 className="text-3xl text-[#c0c0c0] font-extrabold">Hourly Traffic Trend</h1>
                    <div className="chart-container flex justify-center items-center mt-10 w-full border h-96 rounded-lg">
                        <p className="text-6xl font-bold">Trends</p>
                    </div>
                </div>
            </div>

            <div className="traffic_trend_daily mt-20">
                <div className="chart px-20">
                    <h1 className="text-3xl text-[#c0c0c0] font-extrabold">Daily Traffic Trend</h1>
                    <div className="chart-container flex justify-center items-center mt-10 w-full border h-96 rounded-lg">
                        <p className="text-6xl font-bold">Trends</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Analytic;
