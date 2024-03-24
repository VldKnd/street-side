export default function DownloadPeriodComponent() {
    return (
        <div className="border-2 border-company-grey rounded-2xl">
            <div className="m-3">
                <div className="flex">
                    <div className='mb-3 ml-3 mr-3 text-foreground-white text-base'>
                        {"Select a period to download"}
                    </div>
                </div>
                <div className="flex rounded-2xl">
                    <div className="place-self-center text-company-grey mr-4">
                        From:
                    </div>
                    <div className="border-2 border-company-grey flex grow rounded-2xl mr-4">
                        <div className="ml-4 mt-3 mb-2 size-6 w-16" />
                    </div>
                    <div className="place-self-center text-company-grey mr-4">
                        To:
                    </div>
                    <div className="border-2 border-company-grey flex grow rounded-2xl mr-4">
                        <div className="ml-4 mt-3 mb-2 size-6 w-16" />
                    </div>
                    <div className="bg-company-grey flex grow rounded-2xl text-foreground-white">
                        <div className="ml-4 mt-3 mb-2 mr-4">
                            Download
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}