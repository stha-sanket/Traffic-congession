import React from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.jpg";

const Navbar = () => {
    return (
        <>
            <div className="flex sticky top-0 items-center justify-between h-20 p-4 bg-black px-24 z-10 ">
                <div className="logo">
                    <img src={logo} className="w-14 h-14 rounded-full" alt="logo"/>
                </div>
                <div className="nav">
                    <ul className="flex text-[#c0c0c0] text-2xl font-bold gap-5  ">
                        <li className="hover:text-[#00aeef]">
                            <Link to="/">Home</Link>
                        </li>
                        <li className="hover:text-[#00aeef]">
                            <Link to="/analytic">Dashboard</Link>
                        </li>
                        <li className="hover:text-[#00aeef]">
                            <Link to="/traffic-system">Traffic System</Link>
                        </li>
                    </ul>
                </div>
            </div>
        </>
    );
};

export default Navbar;
