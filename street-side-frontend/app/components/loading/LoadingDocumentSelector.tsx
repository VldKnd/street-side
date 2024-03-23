export default function DocumentSelector() {
    return (
        <div className="border-2 border-company-grey rounded-2xl">
            <div className="m-3">
                <div className='mb-3 ml-3 mr-3 text-foreground-white text-base text-opacity-0'>
                    {"Select a document to view"}
                </div>
                <div className="flex grow bg-company-grey rounded-2xl">
                    <div className="ml-4 mt-3 mb-2 size-6" />
                </div>
            </div>
        </div>
    )
}