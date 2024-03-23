import Selector from './Selector';

export default function CompanySelector() {
    return (
        <div>
            <div className='relative w-1000 flex'>
                <div className='mb-3 ml-3'>
                    <text className='text-company-grey text-2xl'>
                        {"Welcome to the streets!"}
                    </text>
                </div>
                <div className='grow' />
                <div className='absolute bottom-0 right-0 mb-3 mr-3 text-foreground-white text-base'>
                    {"Select the clearing company"}
                </div>
            </div>
            <div>
                <Selector />
            </div>
        </div>
    )
}