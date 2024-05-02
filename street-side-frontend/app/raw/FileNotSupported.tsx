'use client';
export function FileNotSupported({ extention, stackOrder
 } : { extention: string, stackOrder: string }) {
    return (
        <div className={`relative flex flex-col justify-center ${stackOrder} text-foreground-white items-center inline-block w-full`}>
            <p>
                Selected document is has {extention} format and can not yet be pre-viewed.
            </p>
            <p>
                You can still download it on your local disk by clicking the 'Download data' button!
            </p>
        </div>
    )
}