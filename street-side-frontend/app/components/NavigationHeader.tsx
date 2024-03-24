
'use client';
import { usePathname } from 'next/navigation';
import Link from "next/link";

function setLinkStyle(isActive: boolean) {
    const activeStyle = "rounded-xl border-solid border-2 border-title-red"
    const inactiveStyle = "hover:font-semibold"
    return `text-xl text-title-red ${isActive ? activeStyle : inactiveStyle}`
}

export default function NavigationHeader() {
    const pathname = usePathname()
    const isHome = pathname === "/home"
    const isRaw = pathname === "/raw"

    return (
        <div className="absolute top-0 left-0 mt-6 ml-6">
            <div className="mb-4">
                <Link href="/home" className="text-3xl text-title-red">
                    {"StreetSide"}
                </Link>
            </div>

            <div className="mb-4 ">
                <Link href="/home" className={setLinkStyle(isHome)}>
                    <text className='m-2'>
                        {"Home"}
                    </text>
                </Link>
            </div>


            <div className="mb-4">
                <Link href="/raw" className={setLinkStyle(isRaw)}>
                    <text className='m-2'>
                        {"Raw data"}
                    </text>
                </Link>
            </div>
        </div >
    );
}