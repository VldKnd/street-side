'use client';
export function FileNotSupported({ extention, stackOrder
 } : { extention: string, stackOrder: string }) {
    return (
        <div className={`relative flex flex-col justify-center ${stackOrder} text-foreground-white items-center inline-block w-full`}>
            <p>
                Selected document have {extention} format and can not be pre-viewed at the moment.
            </p>
            <p>
                You can still download it on your local disk by clicking the &apos;Download data&apos; button!
            </p>
        </div>
    )
}